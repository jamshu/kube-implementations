FROM bitnami/minideb:latest

# Copy the predefined filestore and PostgreSQL data into the image
COPY filestore /backups/filestore
COPY backup/base.tar.gz /backups/base.tar.gz
COPY backup/pg_wal.tar.gz /backups/pg_wal.tar.gz
COPY backup/backup_manifest /backups/backup_manifest
# Copy the restore script into the image
COPY restore.sh /usr/local/bin/restore.sh

# Make the restore script executable
RUN chmod +x /usr/local/bin/restore.sh

ENTRYPOINT ["/bin/bash"]

