# Copyright 2015 Odoo S. A.
# Copyright 2015 Laurent Mignon <laurent.mignon@acsone.eu>
# Copyright 2015 Ronald Portier <rportier@therp.nl>
# Copyright 2016-2017 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64

import dateutil.parser

from odoo import api, models
from odoo.exceptions import UserError
from odoo.tools.translate import _


class AccountStatementImport(models.TransientModel):
    _inherit = "account.statement.import"

    @api.model
    def _check_qif(self, data_file):
        return data_file.strip().startswith(b"!Type:")

    def _parse_file(self, data_file):
        if not self._check_qif(data_file):
            return super()._parse_file(data_file)
        try:
            file_data = data_file.decode()
            if "\r" in file_data:
                data_list = file_data.split("\r")
            else:
                data_list = file_data.split("\n")
            header = data_list[0].strip()
            header = header.split(":")[1]
        except Exception as e:
            raise UserError(_("Could not decipher the QIF file.")) from e
        transactions = []
        vals_line = {}
        total = 0
        if header in ("Bank", "CCard"):
            vals_bank_statement = {}
            for line in data_list:
                line = line.strip()
                if not line:
                    continue
                if line[0] == "D":  # date of transaction
                    vals_line["date"] = dateutil.parser.parse(
                        line[1:], fuzzy=True
                    ).date()
                elif line[0] == "T":  # Total amount
                    total += float(line[1:].replace(",", ""))
                    vals_line["amount"] = float(line[1:].replace(",", ""))
                elif line[0] == "N":  # Check number
                    vals_line["ref"] = line[1:]
                elif line[0] == "P":  # Payee
                    vals_line["payment_ref"] = (
                        "name" in vals_line
                        and line[1:] + ": " + vals_line["name"]
                        or line[1:]
                    )
                elif line[0] == "M":  # Memo
                    vals_line["payment_ref"] = (
                        "name" in vals_line
                        and vals_line["name"] + ": " + line[1:]
                        or line[1:]
                    )
                elif line[0] == "^" and vals_line:  # end of item
                    transactions.append(vals_line)
                    vals_line = {}
                elif line[0] == "\n":
                    transactions = []
                else:
                    pass
        else:
            raise UserError(
                _(
                    "This file is either not a bank statement or is "
                    "not correctly formed."
                )
            )
        vals_bank_statement.update(
            {"balance_end_real": total, "transactions": transactions}
        )
        journal = self.env["account.journal"].browse(self.env.context.get("journal_id"))
        return journal.currency_id.name, None, [vals_bank_statement]

    def _complete_stmts_vals(self, stmt_vals, journal_id, account_number):
        """Match partner_id if hasn't been deducted yet."""
        res = super()._complete_stmts_vals(stmt_vals, journal_id, account_number)
        # Since QIF doesn't provide account numbers (normal behaviour is to
        # provide 'account_number', which the generic module uses to find
        # the partner), we have to find res.partner through the name
        if not self.statement_file or not self._check_qif(
            base64.b64decode(self.statement_file)
        ):
            return res
        partner_obj = self.env["res.partner"]
        for statement in res:
            for line_vals in statement["transactions"]:
                if not line_vals.get("partner_id") and line_vals.get("payment_ref"):
                    partner = partner_obj.search(
                        [("name", "ilike", line_vals["payment_ref"])],
                        limit=1,
                    )
                    line_vals["partner_id"] = partner.id
        return res
