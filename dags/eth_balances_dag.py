from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from datetime import datetime
import csv
from scripts.fetch_eth_balances import fetch_balances


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 8, 13)
}

dag = DAG(
    'ethereum_balances_to_bigquery',
    default_args=default_args,
    schedule='@daily',
)


def extract_and_save_balances(**kwargs):
    balances = fetch_balances()

    file_path = '/tmp/eth_balances.csv'
    with open(file_path, 'w', newline='') as f:
        fieldnames = ['address', 'balance']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for address, balance in balances.items():
            writer.writerow({'address': address, 'balance': balance})

    kwargs['ti'].xcom_push(key='file_path', value=file_path)


extract_balances_task = PythonOperator(
    task_id='extract_balances',
    python_callable=extract_and_save_balances,
    provide_context=True,
    dag=dag,

)

upload_to_gcs_task = LocalFilesystemToGCSOperator(
    task_id='upload_to_gcs',
    # Ensure 'extract_balances' matches the task_id of your previous task
    src="{{ ti.xcom_pull(task_ids='extract_balances', key='file_path') }}",
    dst='eth_balances/eth_balances.csv',
    bucket='eth_project1',
    dag=dag,
)


load_to_bigquery_task = GCSToBigQueryOperator(
    task_id='load_to_bigquery',
    bucket='eth_project1',
    source_objects=['eth_balances/eth_balances.csv'],
    destination_project_dataset_table='airflow-432421.eth_project.eth_info',
    source_format='CSV',
    skip_leading_rows=1,
    write_disposition='WRITE_TRUNCATE',
    autodetect=True,
    gcp_conn_id='google_cloud_default',
    dag=dag,

)

extract_balances_task >> upload_to_gcs_task >> load_to_bigquery_task
