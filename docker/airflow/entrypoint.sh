airflow db migrate

sleep 20

airflow users create \
    --username admin \
    --password admin \
    --firstname admin \
    --lastname admin \
    --role Admin \
    --email admin@admin.com  

airflow webserver --port 8080 & airflow scheduler
