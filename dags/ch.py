from importlib_metadata import metadata
from sqlalchemy import create_engine, Column, MetaData, literal, Integer, DateTime, String

from clickhouse_sqlalchemy import Table, make_session, get_declarative_base, types, engines

uri = "clickhouse://default:@clickhouse_server/polls"
engine = create_engine(uri)
session = make_session(engine)
metadata = MetaData(bind=engine)


Base = get_declarative_base(metadata=metadata)


def get_ch_conn():
    return engine

class Question(Base):
    __tablename__ = "polls_question"
    __table_args__ = (
        engines.MergeTree(order_by=['id']), engines.Memory(),
        # {'schema': database},
    )

    id = Column("id", Integer(), primary_key=True)
    question_text = Column("question_text", String(200))
    pub_date = Column("pub_date", DateTime(),)
