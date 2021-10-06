from dotenv import load_dotenv

load_dotenv()

from landmarks_parser import LandmarkParser

parser = LandmarkParser()

if __name__ == '__main__':
    parser.parse()
