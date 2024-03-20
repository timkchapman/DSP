import os
import configparser

basedir = os.path.abspath(os.path.dirname(__file__))
config_file_path = os.path.join(basedir, 'config.ini')

config = configparser.ConfigParser()
config.read(config_file_path)


class Config:
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')\
		or 'sqlite:///' + os.path.join(basedir, 'LarpBook.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	STATIC_FOLDER = 'Static'
	STATIC_URL_PATH = 'LarpBook/static'

	try:
		GEOCODER_API_KEY = config['API_KEYS']['GEOCODER_API_KEY']
	except KeyError:
		raise KeyError('GEOCODER_API_KEY not found in the configuration file')

	try:
		SECRET_KEY = config['API_KEYS']['SECRET_KEY']
	except KeyError:
		raise KeyError('SECRET_KEY not found in the configuration file')