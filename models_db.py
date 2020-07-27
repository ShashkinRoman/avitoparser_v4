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


class InformationFromAds(Base):
    __tablename__ = os.getenv('ads_tablename')
    id = Column(Integer, primary_key=True)
    phone = Column(String)
    request = Column(String)
    name = Column(String)
    title = Column(String)
    price = Column(String)
    place = Column(String)
    description = Column(String)
    type_ads = Column(String)
    region = Column(String)
    url = Column(String)

    def __init__(self, phone, request, name, title, price, place, description, type_ads, region, url):
        self.phone = phone
        self.request = request
        self.name = name
        self.title = title
        self.price = price
        self.place = place
        self.description = description
        self.type_ads = type_ads
        self.region = region
        self.url = url

    def __repr__(self):
        return "<InformationFromAds('%s','%s', '%s', '%s','%s', '%s', '%s','%s', '%s', '%s')>"\
               % (self.phone, self.request, self.name, self.title,
                  self.price, self.place, self.description,
                  self.type_ads, self.region, self.url)


def session_db():
    engine = create_engine('sqlite:///' + os.getenv('database_name') + '.db',
                           connect_args={'check_same_thread':  False},
                           poolclass=StaticPool)
    session_object = sessionmaker()
    session_object.configure(bind=engine)
    Base.metadata.create_all(engine)
    session = session_object()
    return session