from datetime import datetime
from airflow import DAG 

today = datetime.now()

with DAG(
    "demo",
    start_date=datetime(2021, 1, 1),
    schedule_interval="@daily",
    catchup=False
) as dag:
    
    # Access django models




    # Access clickhouse models


    # Copy the data 

    pass