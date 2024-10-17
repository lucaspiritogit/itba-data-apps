from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from wowtokendag.battle_net_api import get_oauth_access_token, get_wow_token
from wowtokendag.database_functions import create_table, analyze_token_data

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

dag = DAG(
    'wow_token_dag',
    default_args=default_args,
    description='Fetch WoW token data daily',
    schedule_interval='@daily',
    start_date=datetime(2024, 8, 10),
    catchup=True,
    max_active_runs=1
)

create_table_task = PythonOperator(
    task_id='create_table_task',
    python_callable=create_table,
    dag=dag,
)

get_oauth_access_token_task = PythonOperator(
    task_id='get_oauth_access_token_task',
    python_callable=get_oauth_access_token,
    provide_context=True,
    dag=dag,
)

get_wow_token_task = PythonOperator(
    task_id='get_wow_token_task',
    python_callable=get_wow_token,
    provide_context=True,
    dag=dag,
)

analyze_token_data_task = PythonOperator(
    task_id='analyze_token_data_task',
    python_callable=analyze_token_data,
    provide_context=True,
    dag=dag,
)

create_table_task >> get_oauth_access_token_task >> get_wow_token_task >> analyze_token_data_task
