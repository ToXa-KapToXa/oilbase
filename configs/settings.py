from dotenv import load_dotenv
import os

HOST_SERVER = '0.0.0.0'
PORT_SERVER = 9889

FLASK_LOG = True
LOGGING_CFG_PATH = "./configs/logging.cfg.yml"

load_dotenv(dotenv_path="./configs/.credits.env")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_LOGIN = os.getenv("DB_LOGIN")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")