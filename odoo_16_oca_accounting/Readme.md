# install

helm install my-odoo-16 bitnami/odoo --version 23.0.0 -f odoo_16_oca.yaml
helm upgrade --install my-odoo-16 bitnami/odoo --version 23.0.0 -f .\odoo_16_oca.yaml