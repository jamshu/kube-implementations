docker build -t jamshidk/odoo-backup-restore:16.1 .
docker push jamshidk/odoo-backup-restore:16.1  
Add the image name on odoo-restore-job

Install odoo using helm(odoo-16-oca if name change the corresponding pvc name the restore job yaml)

kubectl apply -f odoo-restore-job.yaml

kubectl scale deployment odoo16-oca --replicas=0
kubectl scale statefulset odoo-16-oca-postgresql --replicas=0


# to create a backup using pg_basebackup you need to  make pg_hba entry

kubectl cp ./pg_hba.conf $POSTGRES_POD:/path/to/pg_hba.conf
kubectl exec -it $POSTGRES_POD -- bash -c "PGPASSWORD='$POSTGRES_PASSWORD' psql -U $POSTGRES_USER -c 'SHOW hba_file;'"
psql -U postgres -c 'SHOW hba_file;'

/opt/bitnami/postgresql/conf/pg_hba.conf

kubectl exec -it $POSTGRES_POD -- bash -c "echo 'host    replication     postgres    127.0.0.1/32    md5' | tee -a /opt/bitnami/postgresql/conf/pg_hba.conf"
kubectl exec -it odoo-16-oca-postgresql-0 -- bash -c "echo 'host    replication     postgres    127.0.0.1/3
2      md5' | tee -a /opt/bitnami/postgresql/conf/pg_hba.conf"
kubectl exec -it $POSTGRES_POD -- bash -c "PGPASSWORD='$POSTGRES_PASSWORD' psql -U $POSTGRES_USER -c 'SELECT pg_reload_conf();'"
kubectl exec -it $POSTGRES_POD -- bash -c "pg_basebackup -h 127.0.0.1 -D /tmp/backup -U postgres -Ft -z -Xs -P"

# you can take the postgres user password from secret

kubectl get secret <postgres-secret> -n <namespace> -o jsonpath="{.data.postgres-password}" | base64 --decode
kubectl get secret odoo-16-oca-postgresql  -o jsonpath="{.data.postgres-password}" | base64 --decode