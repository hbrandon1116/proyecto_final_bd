
import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from model.models import (
Base, Idioma, Rol, Autor, Material, MaterialAutor, Copia,
get_engine
)
from model.usuario import *


# Cargar env
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
ROOT_DIR = os.path.dirname(BASE_DIR)                   
ENV_PATH = os.path.join(ROOT_DIR, "config_example.env")

load_dotenv(ENV_PATH)

DB_URL = os.getenv("DB_URL")

if not DB_URL:
    raise RuntimeError("ERROR: No se encontró la variable DB_URL en el archivo .env")

engine = get_engine(DB_URL)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
