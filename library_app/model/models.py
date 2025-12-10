# models.py
import hashlib
from sqlalchemy import (
    create_engine, Column, Integer, String, Date, DateTime, Text,
    ForeignKey, Numeric, CheckConstraint, UniqueConstraint
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.sql import func

Base = declarative_base()

class Idioma(Base):
    __tablename__ = 'idioma'
    id_idioma = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False, unique=True)

class Usuario(Base):
    __tablename__ = 'usuario'
    id_usuario = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(150), nullable=False, unique=True)
    tipo_usuario = Column(String(20), nullable=False)  # 'estudiante','profesor','admin'
    fecha_registro = Column(Date, server_default=func.current_date())
    password_hash = Column(String(200), nullable=True)

    prestamos = relationship("Prestamo", back_populates="usuario")
    reservas = relationship("Reserva", back_populates="usuario")    
def set_password(self, password: str):
        """Crea un hash SHA-256 y lo almacena."""
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()

def check_password(self, password: str) -> bool:
        """Verifica si el hash coincide con la contraseña ingresada."""
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()

class Rol(Base):
    __tablename__ = 'rol'
    id_rol = Column(Integer, primary_key=True)
    nombre = Column(String(50), unique=True, nullable=False)

class UsuarioRol(Base):
    __tablename__ = 'usuario_rol'
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario', ondelete='CASCADE'), primary_key=True)
    id_rol = Column(Integer, ForeignKey('rol.id_rol', ondelete='CASCADE'), primary_key=True)

class Autor(Base):
    __tablename__ = 'autor'
    id_autor = Column(Integer, primary_key=True)
    nombre = Column(String(200), nullable=False)

class Material(Base):
    __tablename__ = 'material'
    id_material = Column(Integer, primary_key=True)
    titulo = Column(String(300), nullable=False, index=True)
    descripcion = Column(Text)
    id_idioma = Column(Integer, ForeignKey('idioma.id_idioma', ondelete='SET NULL'))
    tipo_material = Column(String(50), nullable=False)
    año_publicacion = Column(Integer)
    isbn = Column(String(30))

    autores = relationship("MaterialAutor", back_populates="material")
    copias = relationship("Copia", back_populates="material")

class MaterialAutor(Base):
    __tablename__ = 'material_autor'
    id_material = Column(Integer, ForeignKey('material.id_material', ondelete='CASCADE'), primary_key=True)
    id_autor = Column(Integer, ForeignKey('autor.id_autor', ondelete='CASCADE'), primary_key=True)
    orden = Column(Integer, default=1)

    material = relationship("Material", back_populates="autores")
    autor = relationship("Autor")

class Copia(Base):
    __tablename__ = 'copia'
    id_copia = Column(Integer, primary_key=True)
    id_material = Column(Integer, ForeignKey('material.id_material', ondelete='CASCADE'))
    codigo_copia = Column(String(50), unique=True, nullable=True)
    ubicacion = Column(String(200))
    coleccion = Column(String(100), nullable=True)  # <-- agregado para filtro por colección
    estado = Column(String(20), nullable=False)  # CHECK handled in DB
    formato = Column(String(30), default='fisico')
    fecha_adquisicion = Column(Date, server_default=func.current_date())

    material = relationship("Material", back_populates="copias")
    prestamos = relationship("Prestamo", back_populates="copia")
    reservas = relationship("Reserva", back_populates="copia")

class Prestamo(Base):
    __tablename__ = 'prestamo'
    id_prestamo = Column(Integer, primary_key=True)
    id_copia = Column(Integer, ForeignKey('copia.id_copia', ondelete='RESTRICT'))
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario', ondelete='RESTRICT'))
    fecha_prestamo = Column(Date, server_default=func.current_date())
    fecha_devolucion_prevista = Column(Date, nullable=False)
    fecha_devolucion_real = Column(Date, nullable=True)
    estado = Column(String(20), nullable=False)
    multa = Column(Numeric(8,2), default=0)

    copia = relationship("Copia", back_populates="prestamos")
    usuario = relationship("Usuario", back_populates="prestamos")

class Reserva(Base):
    __tablename__ = 'reserva'
    id_reserva = Column(Integer, primary_key=True)
    id_copia = Column(Integer, ForeignKey('copia.id_copia', ondelete='RESTRICT'))
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario', ondelete='RESTRICT'))
    fecha_reserva = Column(DateTime, server_default=func.now())
    estado = Column(String(20), nullable=False)

    copia = relationship("Copia", back_populates="reservas")
    usuario = relationship("Usuario", back_populates="reservas")

class Movimiento(Base):
    __tablename__ = 'movimiento'
    id_movimiento = Column(Integer, primary_key=True)
    id_copia = Column(Integer, ForeignKey('copia.id_copia', ondelete='SET NULL'), nullable=True)
    accion = Column(String(50), nullable=False)
    fecha = Column(DateTime, server_default=func.now())
    detalle = Column(Text)

# helper to create engine/session externally
def get_engine(connection_string):
    return create_engine(connection_string, echo=False, future=True)

def get_session(engine):
    return sessionmaker(bind=engine, autoflush=False, future=True)()

