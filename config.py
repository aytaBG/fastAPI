from dotenv import load_dotenv
import os

# забор данных из файла .env
load_dotenv()

# получаем переменные из .env
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
SECRETA = os.environ.get('SECRETA')
SECRETM = os.environ.get('SECRETM')