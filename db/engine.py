import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


class Engine(object):
    __instance = None
    __engine = None
    __declarative_base = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__engine = create_engine(
                'postgresql+psycopg2://{user}:{password}}@{host}:{port}/{db_name}'.format(
                    user=os.getenv('DB_USER'),
                    password=os.getenv('DB_PASSWORD'),
                    host=os.getenv('DB_HOST'),
                    port=os.getenv('DB_PORT'),
                    db_name=os.getenv('DB_NAME')
                ), echo=True)
            cls.__declarative_base = declarative_base()
            cls.__instance = super(Engine, cls).__new__(cls)

        return cls
