
from model.models import (
    get_engine, get_session, Material, Copia, Prestamo, Reserva
)
from model.usuario import Usuario
from sqlalchemy import select, and_, or_, func
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


class AuthController:
    def __init__(self, session: Session):
        self.session = session
        self.current_user = None

  
    def login(self, usuario: str, password: str) -> bool:
        if not usuario or not password:
            return False

        user = (
            self.session.query(Usuario)
            .filter(Usuario.nombre == usuario)
            .first()
        )

        if user and user.check_password(password):
            self.current_user = user
            return True

        return False



    def register(self, nombre: str, correo: str, password: str, tipo_usuario="estudiante"):
        """Registra un usuario nuevo con contraseña encriptada."""
        nuevo = Usuario(
            nombre=nombre,
            correo=correo,
            tipo_usuario=tipo_usuario
        )
        nuevo.set_password(password)

        try:
            self.session.add(nuevo)
            self.session.commit()
            return True
        except IntegrityError:
            self.session.rollback()
            return False


    def logout(self):
        self.current_user = None

    def get_current_user(self):
        return self.current_user

