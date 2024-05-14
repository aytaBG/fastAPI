from dotenv import load_dotenv
import os

# забор данных из файла .env
load_dotenv()

# получаем переменные из .env
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_NAME_TEST = os.environ.get('DB_NAME_TEST')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')

REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')

SECRETA = os.environ.get('SECRETA')
SECRETM = os.environ.get('SECRETM')

SMTP_USER = os.environ.get('SMTP_USER')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')
