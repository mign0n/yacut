import os

from string import ascii_letters, digits

ORIGINAL_LINK_PATTERN = (
    r'^[a-z]+://'
    r'(?P<host>[^\/\?:]+)'
    r'(?P<port>:[0-9]+)?'
    r'(?P<path>\/.*?)?'
    r'(?P<query>\?.*)?$'
)
SHORT_CHARACTERS = ascii_letters + digits
SHORT_PATTERN = r'[{}]+'.format(SHORT_CHARACTERS)
SHORT_VIEW = 'short_url_view'


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'SUP$R-SECR3T-KEY')

    DEFAULT_SHORT_SIZE = 6
    ORIGINAL_LINK_MAX_SIZE = 2000
    SHORT_MAX_SIZE = 16

    MAX_ITERATION = 10
