from sqlalchemy.orm import sessionmaker
from model.db import engine
from model.models import Rol  

Session = sessionmaker(bind=engine)
session = Session()

roles = [
    {"nombre": "estudiante"},
    {"nombre": "profesor"},
    {"nombre": "bibliotecario"},
]

for r in roles:
    exists = session.query(Rol).filter_by(nombre=r["nombre"]).first()
    if not exists:
        role = Rol(nombre=r["nombre"])
        session.add(role)

session.commit()
print("✔️ Roles creados correctamente")
