from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from models.main import Base


class Fact(Base):
    __tablename__ = 'Facts'

    id_fact = Column(Integer, primary_key=True)
    description = Column(Text, nullable=False)
    id_landmark = Column(Integer, ForeignKey("Landmarks.id_author"))
    Landmark = relationship("Landmark")

