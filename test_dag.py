from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 3, 25),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': True,
    'email_on_retry': True,
    'email': ['admin@example.com'],
}


dag = DAG(
    'dummy_dag',
    default_args=default_args,
    schedule_interval=timedelta(hours=1),
)


def write_to_log(**kwargs):
    with open('/tmp/dummy_log.txt', 'a') as file:
        file.write('Dummy DAG ran at ' + str(datetime.now()) + '\n')


def on_failure_callback(context):
    # Handle failure
    pass


def on_success_callback(context):
    print('DAG Successful')


dummy_task1 = PythonOperator(
    task_id='write_to_log',
    python_callable=write_to_log,
    on_failure_callback=on_failure_callback,
    dag=dag
)


dummy_task2 = DummyOperator(
    task_id='dummy_task2',
    dag=dag
)


dummy_task3 = DummyOperator(
    task_id='dummy_task3',
    trigger_rule='all_done',
    on_success_callback=on_success_callback,
    dag=dag
)


dummy_task1 >> dummy_task2 >> dummy_task3