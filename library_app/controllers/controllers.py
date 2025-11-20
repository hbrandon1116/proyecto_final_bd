# controllers.py
from model.models import (
    get_engine, get_session, Material, Copia, Usuario, Prestamo, Reserva
)
from sqlalchemy import select, and_, or_, func

class LibraryController:
    def __init__(self, connection_string):
        self.engine = get_engine(connection_string)
        self.session = get_session(self.engine)

    def init_db(self):
        # Crea tablas si no existen
        from model.models import Base
        Base.metadata.create_all(self.engine)

    # --- Public search (sin login) ---
    def search_public(self, q_text=None, codigo=None, isbn=None, coleccion=None, estado='disponible'):
        s = select(Copia).join(Material).options()
        filters = []
        if codigo:
            filters.append(Copia.codigo_copia == codigo)
        if q_text:
            t = f"%{q_text}%"
            filters.append(or_(Material.titulo.ilike(t), Material.descripcion.ilike(t)))
        if isbn:
            filters.append(Material.isbn == isbn)
        if coleccion:
            filters.append(Copia.coleccion == coleccion)
        if estado:
            filters.append(Copia.estado == estado)
        if filters:
            s = s.where(and_(*filters))
        s = s.limit(200)
        return self.session.execute(s).scalars().all()

    # --- Authentication (simple) ---
    def find_user_by_email(self, correo):
        return self.session.execute(select(Usuario).where(Usuario.correo==correo)).scalar_one_or_none()

    # --- For logged users: prestamos, reservas, multas ---
    def get_prestamos_by_user(self, user_id):
        s = select(Prestamo).where(Prestamo.id_usuario==user_id).order_by(Prestamo.fecha_prestamo.desc())
        return self.session.execute(s).scalars().all()

    def get_reservas_by_user(self, user_id):
        s = select(Reserva).where(Reserva.id_usuario==user_id).order_by(Reserva.fecha_reserva.desc())
        return self.session.execute(s).scalars().all()

    def pay_multa(self, prestamo_id):
        # Simula pago: pone multa a 0 en el préstamo y guarda movimiento
        p = self.session.get(Prestamo, prestamo_id)
        if not p:
            return False
        p.multa = 0
        self.session.add(p)
        self.session.commit()
        return True

