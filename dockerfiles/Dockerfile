# FROM puckel/docker-airflow:latest
FROM apache/airflow:2.2.5
RUN pip install requests
RUN pip install pandas \
    && pip install pymysql \
    && pip install ipython \
    && pip install clickhouse-sqlalchemy
RUN airflow db init
RUN airflow scheduler -D
# RUN airflow users create \
#     --username admin \
#     --firstname Peter \
#     --lastname Parker \
#     --role Admin \
#     --email spiderman@superhero.org
 