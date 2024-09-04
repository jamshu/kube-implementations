docker build -t jamshidk/odoo:16.0-oca-accounting .
docker push jamshidk/odoo:16.0-oca-accounting
helm install odoo-16-oca bitnami/odoo --version 23.0.0 -f values.yaml