# controllers.py

from model.models import (
    get_engine, get_session, Material, Copia, Prestamo, Reserva
)

from model.usuario import Usuario
from sqlalchemy import select, and_, or_, func
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
