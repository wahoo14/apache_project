from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import timedelta


with DAG(
    dag_id= 'APACHE_consumer_standalone',
    description='standalone dag to consumer data from the LazerScan topic.',
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

consumer_task

if __name__ == "__main__":
    dag.test()