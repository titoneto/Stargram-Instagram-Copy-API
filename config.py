import os.path
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'storage.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = 'vb89e45huv79bz8cn7hftwe7wqt5o7gks24dvm9lçl1nask'