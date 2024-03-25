import os
import configparser

basedir = os.path.abspath(os.path.dirname(__file__))
config_file_path = os.path.join(basedir, 'configuration.ini')

config = configparser.ConfigParser()
config.read(config_file_path)


class Config:
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')\
		or 'sqlite:///' + os.path.join(basedir, 'LarpBook.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	STATIC_FOLDER = 'Static'
	STATIC_URL_PATH = 'LarpBook/static'
	SESSION_TYPE = 'filesystem'

	WTF_CSRF_ENABLED = True

	try:
		GEOCODER_API_KEY = config['API_KEYS']['GEOCODER_API_KEY']
	except KeyError:
		raise KeyError('GEOCODER_API_KEY not found in the configuration file')

	try:
		SECRET_KEY = config['API_KEYS']['SECRET_KEY']
	except KeyError:
		raise KeyError('SECRET_KEY not found in the configuration file')
	
	try:
		STRIPE_KEY = config['API_KEYS']['STRIPE_KEY']
	except KeyError:
		raise KeyError('STRIPE_KEY not found in the configuration file')