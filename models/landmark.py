from sqlalchemy import Column, Integer, String, Text, ARRAY
from sqlalchemy.orm import relationship

from db.engine import Engine

dbase = Engine()
engine = dbase.__engine
Base = dbase.__declarative_base


class Landmark(Base):
    __tablename__ = 'Landmarks'

    id_landmark = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    slug = Column(String(250), nullable=False)
    source = Column(String(250), nullable=False)
    description = Column(Text, nullable=False)
    images = ARRAY(String),
    fact = relationship('Fact')


Base.metadatBase.metadata.create_all(engine)
