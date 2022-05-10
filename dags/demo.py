from datetime import datetime
from airflow import DAG 
from airflow.operators.python import PythonOperator

from dj.classes import get_django_conn, Question
from ch import get_ch_conn, Question as ChQuestion
from sqlalchemy.orm import sessionmaker

today = datetime.now()

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


def _connect_to_django_db():
    
    engine = get_django_conn()
    engine.connect()
    
    Session = sessionmaker(bind=engine)
    session = Session()

    print("This is mind bogging")
    for q in session.query(Question).all():
        print(q.id)
        print(q.question_text)


def _connect_click_house():
    engine = get_ch_conn()
    engine.connect()

    session = sessionmaker(engine)()

    print("This is thundersome")
    for q in session.query(ChQuestion).all():
        print(q.id)
        print(q.question_text)
    # pass


def _copy_data():
    engine_for_dj = get_django_conn()
    engine_for_ch = get_ch_conn()

    dj_session = sessionmaker(bind=engine_for_dj)()
    ch_session = sessionmaker(engine_for_ch)()

    for q in dj_session.query(Question).all():
        # ch
        ch_q = ch_session.query(ChQuestion).filter_by(id=q.id).first()

        if ch_q:
            ch_q.question_text = q.question_text
        else:
            ch_q = ChQuestion(
                id=q.id, 
                question_text=q.question_text, 
                pub_date=q.pub_date
            )

        ch_session.add(ch_q)
    ch_session.commit()


with DAG(
    "demo",
    start_date=datetime(2021, 1, 1),
    schedule_interval="@daily",
    catchup=False
) as dag:
    
    # Access django models
    django = PythonOperator(
        task_id="django",
        python_callable=_connect_to_django_db,
        dag=dag
    )


    # Access ch models
    click_house = PythonOperator(
        task_id="click_house",
        python_callable=_connect_click_house,
        dag=dag
    )


    # Copy data
    copy_data = PythonOperator(
        task_id="copy_data",
        python_callable=_copy_data,
        dag=dag
    )

    [django, click_house] >> copy_data
