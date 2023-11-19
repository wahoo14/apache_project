from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import timedelta


with DAG(
    dag_id= 'APACHE_combined_pipeline',
    description='Ingestion and consumption, pushing data into kafka and consuming into spark streaming.',
    schedule_interval=None,
    start_date=days_ago(2),
    catchup=False,
    tags=['Apache Data Engineering Project'],
    default_args={
        'owner': 'airflow',
        'email': ['airflow@example.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 0,
        'depends_on_past': False,
        'retry_delay': timedelta(minutes=5)
    }
) as dag:
    start_dag = DummyOperator(
        task_id='start_dag'
        )
    
    end_dag = DummyOperator(
        task_id='end_dag'
        )        

    ingest_task = DockerOperator(
        task_id='ingest',
        image='ingest',
        api_version='auto',
        auto_remove=True,
        mount_tmp_dir=False,
        container_name='ingest',
        docker_url='tcp://docker-proxy:2375',
        network_mode='apache_datapipeline'
    )

    consumer_task = DockerOperator(
        task_id='consumer',
        image='consumer',
        api_version='auto',
        auto_remove=True,
        mount_tmp_dir=False,
        container_name='consumer',
        docker_url='tcp://docker-proxy:2375',
        network_mode='apache_datapipeline'
    )


    start_dag >> ingest_task
    start_dag >> consumer_task
    ingest_task >> end_dag
    consumer_task >> end_dag


if __name__ == "__main__":
    dag.test()