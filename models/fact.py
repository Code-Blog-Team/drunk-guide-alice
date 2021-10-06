from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from db.engine import Engine

dbase = Engine()
engine = dbase.__engine
Base = dbase.__declarative_base


class Fact(object):
    __tablename__ = 'Facts'

    id_fact = Column(Integer, primary_key=True)
    description = Column(Text, nullable=False)
    id_landmark = Column(Integer, ForeignKey("Landmarks.id_author"))
    Landmark = relationship("Landmark")


Base.metadata.create_all(engine)
