from os import getenv

from dotenv import load_dotenv

class Settings:
    def __init__(self):
        load_dotenv()
        self.max_token = getenv('MAX_TOKEN')
        self.yandex_token = getenv('YANDEX_TOKEN')
        self.giga_token = getenv('GIGA_TOKEN')
