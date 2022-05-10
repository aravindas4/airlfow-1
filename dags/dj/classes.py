from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    create_engine, Column, String, Integer, literal, DateTime, ForeignKey
)




# from clickhouse_sqlalchemy import engines

# django_uri = "clickhouse://default:@clickhouse_server/polls"
django_uri = "mysql+pymysql://root:mauFJcuf5dhRMQrjj@db/polls?port=33000"

engine = create_engine(django_uri)
session = sessionmaker(engine)()


Base = declarative_base()


def get_django_conn():
    from sqlalchemy import create_engine
    django_uri = "mysql+pymysql://root:mauFJcuf5dhRMQrjj@db/polls?port=3306"
    connect_args= dict(host='db', port=3306)
    engine = create_engine(django_uri, connect_args=connect_args)
    return engine


# Django
class Question(Base):
    __tablename__ = "polls_question"
    # __table_args__ = (
    #     engines.MergeTree(order_by=['id']), engines.Memory(),
    #     # {'schema': database},
    # )

    id = Column("id", Integer(), primary_key=True)
    question_text = Column("question_text", String(200))
    pub_date = Column("pub_date", DateTime(),)


class Choice(Base):
    __tablename__ = "polls_choice"
    # __table_args__ = (
    #     engines.MergeTree(order_by=['id']), engines.Memory(),
    #     # {'schema': database},
    # )

    id = Column("id", Integer(), primary_key=True)
    question_id = Column("question_id", Integer, )

    # question = relationship("Question")

    choice_text = Column("choice_text", String(200))
    votes = Column("votes", Integer(), default=0)


