from db.engine import Engine

dbase = Engine()
engine = dbase.engine
Base = dbase.declarative_base

Base.metadata.create_all(engine)
