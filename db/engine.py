import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


class Engine:
    __instance = None
    engine = None
    declarative_base = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.engine = create_engine(
                'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}'.format(
                    user="Yandex_Hackaton",
                    password="C0deB10g",
                    host="178.151.51.160",
                    port=5432,
                    db_name="Yandex_Hackaton"
                ), echo=True)
            cls.declarative_base = declarative_base()
            cls.__instance = super(Engine, cls).__new__(cls)

        return cls

