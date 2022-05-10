# Importts
from airflow import DAG 
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from datetime import datetime

from random import randint

from airflow.operators.bash_operator import BashOperator
from airflow.utils.task_group import TaskGroup


def _training_model():
    return randint(1, 10)


def _choose_best_model(**kwargs):
    ti = kwargs['ti']
    accuracies = ti.xcom_pull(task_ids=[
        "training_model_A",
        "training_model_B",
        "training_model_C"
    ])

    best_accuracy = max(accuracies)

    if best_accuracy > 5:
        return "accurate"
    
    return "inaccurate"


with DAG(
    "my_dag",
    start_date=datetime(2021, 1, 1),
    schedule_interval="@daily",
    catchup=False
) as dag:
    

    with TaskGroup("processing_ttasks", ) as processing_tasks:
        training_model_A = PythonOperator(
            task_id="training_model_A",
            python_callable=_training_model
        )

        training_model_B = PythonOperator(
            task_id="training_model_B",
            python_callable=_training_model
        )

        training_model_C = PythonOperator(
            task_id="training_model_C",
            python_callable=_training_model
        )

    choose_best_model = BranchPythonOperator(
        task_id="choose_best_model",
        python_callable=_choose_best_model,
        provide_context=True
    )

    with TaskGroup("bash_ttasks", ) as bash_tasks:
        accurate = BashOperator(
            task_id="accurate",
            bash_command="echo 'accurate'"
        )
        inaccurate = BashOperator(
            task_id="inaccurate",
            bash_command="echo 'inaccurate'"
        )

    processing_tasks >> choose_best_model >> bash_tasks
