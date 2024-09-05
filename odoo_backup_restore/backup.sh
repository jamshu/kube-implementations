#!/bin/bash

# Variables
BACKUP_DIR="/backup"
DATE=$(date +%Y%m%d_%H%M%S)
ODOO_POD=$(kubectl get pods -l app.kubernetes.io/name=odoo -o jsonpath="{.items[0].metadata.name}")
POSTGRES_POD=$(kubectl get pods -l app.kubernetes.io/name=postgresql -o jsonpath="{.items[0].metadata.name}")
POSTGRES_USER="bn_odoo"
POSTGRES_PASSWORD="JpatPpPJlM"
POSTGRES_DB="bitnami_odoo"


# Backup Odoo filestore
echo "Backing up Odoo filestore..."
kubectl cp $ODOO_POD:/bitnami/odoo/data/filestore ./filestore

# Backup PostgreSQL data
echo "Backing up PostgreSQL database..."
kubectl cp $POSTGRES_POD:/tmp/backup ./backup
# # Optional: Upload backups to S3
# echo "Uploading backups to S3..."
# aws s3 cp $BACKUP_DIR/odoo-filestore-$DATE s3://$S3_BUCKET/odoo-filestore-$DATE --recursive
# aws s3 cp $BACKUP_DIR/postgres-backup-$DATE.sql s3://$S3_BUCKET/postgres-backup-$DATE.sql

# # Cleanup old backups
# echo "Cleaning up old backups..."
# find $BACKUP_DIR -type f -mtime +7 -exec rm {} \;
