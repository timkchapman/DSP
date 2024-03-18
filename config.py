import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY')
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')\
		or 'sqlite:///' + os.path.join(basedir, 'LarpBook.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	GEOCODER_API_KEY = 'AIzaSyAknTozLR6kcm24rkpgc8kdykbUv8hSTeU'