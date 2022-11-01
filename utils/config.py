from dotenv import load_dotenv
from os import environ

load_dotenv()


class Config:
    CHROME_PATH = environ["CHROME_PATH"]
    HEADLESS = True if environ["HEADLESS"].upper() == "TRUE" else False
