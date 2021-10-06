import os
import pathlib
from sqlalchemy.orm import sessionmaker
from bs4 import BeautifulSoup as BS
from urllib.request import urlopen, urlretrieve

from db.engine import Engine
from models.landmark import Landmark
from models.fact import Fact
from constants.landmark_parser_constants import TARGET_URL, MAIN_PAGE
from utils.text_helpers import make_slug


class LandmarkParser:
    def __init__(self):
        dbase = Engine()
        engine = dbase.__engine
        session = sessionmaker(bind=engine)
        self.session = session()
        self.__parser = 'html.parser'

    async def get_landmarks_list(self):
        result = []
        try:
            resp = await urlopen(TARGET_URL + MAIN_PAGE).read()
            html = await BS(resp, self.__parser)
            items = html.select('.contentpagetitle')
            for item in items:
                name = item.text
                source = MAIN_PAGE + item['href']
                f_resp = await urlopen(source).read()
                f_html = await BS(f_resp, self.__parser)
                container = f_html.select('.contentpaneopen')[1]
                images_src = [TARGET_URL + image['src'] for image in container.select('img')]
                images = [os.path.join(pathlib.Path().parent.parent.resolve(), os.getenv('IMAGE_DIRECTORY')) + image['src'] for image in container.select('img')]
                facts = [p.text for p in container.select('p')]
                description = facts.pop(0)
                result.append({
                    name,
                    source,
                    images,
                    images_src,
                    description,
                    facts,
                })
            return result
        except Exception as err:
            raise Exception('LandmarkParser.get_landmarks_list', err.__class__, 'occurred.')

    async def __save_landmark(self, d_landmark):
        try:
            exist = await self.session.query(Landmark).filter_by(Landmark.slug == make_slug(d_landmark.name)).one()
            if exist:
                exist.source = d_landmark.source
                exist.images = d_landmark.images
                exist.description = d_landmark.description
            else:
                exist = Landmark(
                    name=d_landmark.name,
                    slug=make_slug(d_landmark.name),
                    source=d_landmark.source,
                    description=d_landmark.description,
                    images=d_landmark.images
                )

            self.session.add(exist)
            self.session.commit()
            return exist.id_landmark
        except Exception as err:
            raise Exception('LandmarkParser.__save_landmark', err.__class__, 'occurred.')

    async def __save_landmark_facts(self, landmark_id, facts=None):
        if facts is None:
            facts = []
        try:
            exists = await self.session.query(Fact).filter_by(Fact.id_landmark == landmark_id)
            if exists:
                for fact in exists:
                    self.session.delete(fact)
                await self.session.commit()
            for fact in facts:
                new_fact = Fact(
                    description=fact,
                    id_landmark=landmark_id
                )
                self.session.add(new_fact)
            await self.session.commit()
        except Exception as err:
            raise Exception('LandmarkParser.__save_landmark_facts', err.__class__, 'occurred.')

    async def __save_landmark_images(self, images_urls=None, images=None):
        if images is None:
            images = []
        if images_urls is None:
            images_urls = []
        try:
            for i, url in enumerate(images_urls):
                k = urlretrieve(url, images[i])

        except Exception as err:
            raise Exception('LandmarkParser.__save_landmark_images', err.__class__, 'occurred.')

    async def parse(self):
        try:
            data = await self.get_landmarks_list()
            for landmark in data:
                landmark_id = await self.__save_landmark(landmark)
                await self.__save_landmark_facts(landmark_id, landmark.facts)
                await self.__save_landmark_images(landmark.images_src, landmark.images)
        except Exception as err:
            raise Exception('LandmarkParser.parse', err.__class__, 'occurred.')
