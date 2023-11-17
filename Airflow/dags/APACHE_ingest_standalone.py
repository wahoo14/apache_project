from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import timedelta


with DAG(
    dag_id= 'APACHE_ingest_standalone',
    description='standalone dag for pushing lidar data into the LazerScan kafka topic.',
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

    docker_test_task = DockerOperator(
        task_id='ingest',
        image='ingest',
        api_version='auto',
        auto_remove=True,
        mount_tmp_dir=False,
        container_name='ingest',
        docker_url='tcp://docker-proxy:2375',
        network_mode='apache_datapipeline'
    )

docker_test_task

if __name__ == "__main__":
    dag.test()