from dotenv import load_dotenv
import asyncio

load_dotenv()

from landmarks_parser import LandmarkParser

parser = LandmarkParser()

if __name__ == '__main__':
    asyncio.run(parser.parse())
