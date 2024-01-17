import os

from string import ascii_letters, digits

SHORT_URL_VIEW = 'short_url_view'


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'SUP$R-SECR3T-KEY')

    DEFAULT_SHORT_ID_SIZE = 6
    ORIGINAL_LINK_MAX_SIZE = 2000
    SHORT_ID_CHARACTERS = ascii_letters + digits
    SHORT_ID_MAX_SIZE = 16
    SHORT_ID_PATTERN = r'[{}]+'.format(SHORT_ID_CHARACTERS)

    MAX_ITERATION = 10
