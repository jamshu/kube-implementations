#!/bin/bash


BACKUP_DIR="/backups"
ODOO_DIR="/bitnami/odoo/data/filestore"
DATA_DIR="/bitnami/postgresql/data"

# delete existing data
rm -rf $ODOO_DIR/*
rm -rf $DATA_DIR/*

# Restore Odoo filestore from predefined data in the image (from /backups)
cp -r /backups/filestore/* $ODOO_DIR/
chown -R odoo:odoo $DATA_DIR

# Restore PostgreSQL data directory from predefined data in the image (from /backups)
# Step 1: Restore PostgreSQL backup
echo "Cleaning up existing PostgreSQL data..."
rm -rf $DATA_DIR/*

echo "Restoring PostgreSQL base backup..."
tar -xzf $BACKUP_DIR/base.tar.gz -C $DATA_DIR

echo "Restoring PostgreSQL WAL files..."
tar -xzf $BACKUP_DIR/pg_wal.tar.gz -C $DATA_DIR/pg_wal
touch $DATA_DIR/recovery.signal

echo "Setting PostgreSQL data permissions..."
chown -R 1001:1001 $DATA_DIR

# Print success message
echo "Restore from backup completed successfully."
