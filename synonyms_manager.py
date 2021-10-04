import random

from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import mapper
from sqlalchemy.orm import sessionmaker

from synonyms_finder import SynonymsFinder


class Word(object):
    def __init__(self, word, synonym_id, fact_id):
        self.word = word
        self.synonym_id = synonym_id
        self.fact_id = fact_id

    def __repr__(self):
        return "Word('%s','%s' '%s')" % (self.word, self.synonym_id, self.fact_id)


class SynonymsManager(object):

    def __init__(self):
        engine = create_engine(
            "postgresql+psycopg2://Yandex_Hackaton:C0deB10g@178.151.51.160:5432/Yandex_Hackaton", echo=True)
        metadata = MetaData()
        words_table = Table('words', metadata,
                            Column('id', Integer, primary_key=True),
                            Column('fact_id', Integer),
                            Column('synonym_id', Integer),
                            Column('word', String(30)),
                            )
        metadata.create_all(engine)
        mapper(Word, words_table)
        self.synonyms_finder = SynonymsFinder()
        self.engine = engine
        self.session = sessionmaker(bind=engine)
        self.session.configure(bind=engine)

    def __is_word_suitable_to_rename(self, word):
        return len(word) <= 2

    def cache_text(self, text, text_id):
        session = self.session()

        stmt = select(Word).where((Word.fact_id == text_id))
        if len(session.execute(stmt).all()) != 0:
            return

        words = text.split(" ")
        for i in range(len(words)):
            if self.__is_word_suitable_to_rename(words[i]):
                continue
            synonyms = self.synonyms_finder.get_synonyms(words[i], 0.09)
            synonyms = list(map(lambda x: Word(x, i, text_id), synonyms))
            for synonym in synonyms:
                session.add(synonym)
        session.commit()

    def get_changed_text(self, text, text_id):
        session = self.session()
        words = text.split(" ")
        for i in range(len(words)):
            if self.__is_word_suitable_to_rename(words[i]):
                continue
            stmt = select(Word).where((Word.fact_id == text_id) & (Word.synonym_id == i))
            result = session.execute(stmt).all()
            result = random.choice(result)
            result = result._mapping['Word'].word
            if words[i][0].isupper():
                result = result[0].upper() + result[1:]
            words[i] = result
        return " ".join(words)
