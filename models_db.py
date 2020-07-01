import os
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
load_dotenv()


Base = declarative_base()


class UrlsForParse(Base):
    __tablename__ = os.getenv('tablename')
    id = Column(Integer, primary_key=True)
    region = Column(String)
    request = Column(String)
    date = Column(DateTime)
    url = Column(String)
    status = Column(Integer)


def session_db():
    engine = create_engine('sqlite:///' + os.getenv('database_name') + '.db',
                           connect_args={'check_same_thread':  False},
                           poolclass=StaticPool)
    session_object = sessionmaker()
    session_object.configure(bind=engine)
    Base.metadata.create_all(engine)
    session = session_object()
    return session