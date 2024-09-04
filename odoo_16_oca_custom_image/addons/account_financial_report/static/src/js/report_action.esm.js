/** @odoo-module **/
import {ReportAction} from "@web/webclient/actions/reports/report_action";
import {patch} from "web.utils";
import {useEnrichWithActionLinks} from "./report.esm";

const MODULE_NAME = "account_financial_report";

patch(ReportAction.prototype, "account_financial_report.ReportAction", {
    setup() {
        this._super.apply(this, arguments);
        this.isAccountFinancialReport = this.props.report_name.startsWith(
            `${MODULE_NAME}.`
        );
        useEnrichWithActionLinks(this.iframe);
    },

    export() {
        this.action.doAction({
            type: "ir.actions.report",
            report_type: "xlsx",
            report_name: this._get_xlsx_name(this.props.report_name),
            report_file: this._get_xlsx_name(this.props.report_file),
            data: this.props.data || {},
            context: this.props.context || {},
            display_name: this.title,
        });
    },

    /**
     * @param {String} str
     * @returns {String}
     */
    _get_xlsx_name(str) {
        if (!_.isString(str)) {
            return str;
        }
        const parts = str.split(".");
        return `a_f_r.report_${parts[parts.length - 1]}_xlsx`;
    },
});
