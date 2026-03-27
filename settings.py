import os


class Config(object):
    DROPBOX_TOKEN = os.getenv('DROPBOX_TOKEN')
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
