import os
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.environ.get('MAIL_USERNAME')
PASSWORD = os.environ.get('MAIL_PASSWORD')
HOST = os.environ.get('MAIL_HOST')
PORT = os.environ.get('MAIL_PORT', 465)

AUTH_SECRET_KEY = os.environ.get('AUTH_SECRET_KEY')
AUTH_ALGORITHM = os.environ.get('AUTH_ALGORITHM')
