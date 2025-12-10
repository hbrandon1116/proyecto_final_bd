import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Cargar env
#load_dotenv("config_example.env")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # carpeta model
ROOT_DIR = os.path.dirname(BASE_DIR)                   # sube un nivel
ENV_PATH = os.path.join(ROOT_DIR, "config_example.env")

load_dotenv(ENV_PATH)

DB_URL = os.getenv("DB_URL")

if not DB_URL:
    raise RuntimeError("ERROR: No se encontró la variable DB_URL en el archivo .env")

engine = create_engine(DB_URL, echo=False)
