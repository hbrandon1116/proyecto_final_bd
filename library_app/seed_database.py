import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from model.models import (
Base, Idioma, Rol, Usuario, Autor, Material, MaterialAutor, Copia,
get_engine
)

def seed_database():
    load_dotenv("config_example.env")
    # Leer la URL de conexión a PostgreSQL desde .env
    db_url = os.getenv("DB_URL")

    if not db_url:
        print("ERROR: No se encontró DB_URL en .env")
        return

    engine = get_engine(db_url)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    print("\n=== Ejecutando seed de la base de datos ===")

    # ---------------------------
    #   Poblar Idiomas
    # ---------------------------
    if session.query(Idioma).count() == 0:
        idiomas = [
            Idioma(nombre="Español"),
            Idioma(nombre="Inglés"),
            Idioma(nombre="Francés")
        ]
        session.add_all(idiomas)
        print("✔ Idiomas insertados")

    # ---------------------------
    # 2️⃣ Poblar Roles
    # ---------------------------
    if session.query(Rol).count() == 0:
        roles = [
            Rol(nombre="admin"),
            Rol(nombre="estudiante"),
            Rol(nombre="profesor")
        ]
        session.add_all(roles)
        print("✔ Roles insertados")

    # ---------------------------
    #  Poblar Usuarios
    # ---------------------------
    if session.query(Usuario).count() == 0:
        users = [
            Usuario(nombre="Admin", correo="admin@demo.com", tipo_usuario="admin"),
            Usuario(nombre="Juan Pérez", correo="juan@demo.com", tipo_usuario="estudiante"),
            Usuario(nombre="Ana Gómez", correo="ana@demo.com", tipo_usuario="profesor")
        ]
        session.add_all(users)
        print("✔ Usuarios insertados")

    # ---------------------------
    # Poblar Autores
    # ---------------------------
    if session.query(Autor).count() == 0:
        autores = [
            Autor(nombre="Gabriel García Márquez"),
            Autor(nombre="Antoine de Saint-Exupéry"),
            Autor(nombre="Miguel de Cervantes")
        ]
        session.add_all(autores)
        print("✔ Autores insertados")

    session.commit()

    # Necesitamos IDs para vínculos
    espanol = session.query(Idioma).filter_by(nombre="Español").first()
    ingles = session.query(Idioma).filter_by(nombre="Inglés").first()

    autor_gabo = session.query(Autor).filter_by(nombre="Gabriel García Márquez").first()
    autor_princi = session.query(Autor).filter_by(nombre="Antoine de Saint-Exupéry").first()

    # ---------------------------
    # Poblar Materiales
    # ---------------------------
    if session.query(Material).count() == 0:
        materiales = [
            Material(
                titulo="Cien Años de Soledad",
                tipo_material="libro",
                año_publicacion=1967,
                id_idioma=espanol.id_idioma
            ),
            Material(
                titulo="El Principito",
                tipo_material="libro",
                año_publicacion=1943,
                id_idioma=ingles.id_idioma
            )
        ]
        session.add_all(materiales)
        session.flush()  # para obtener IDs

        # Relación MaterialAutor
        session.add_all([
            MaterialAutor(id_material=materiales[0].id_material, id_autor=autor_gabo.id_autor),
            MaterialAutor(id_material=materiales[1].id_material, id_autor=autor_princi.id_autor)
        ])

        print("✔ Materiales insertados")

    session.commit()

    # ---------------------------
    # Poblar Copias
    # ---------------------------
    if session.query(Copia).count() == 0:
        material1 = session.query(Material).filter_by(titulo="Cien Años de Soledad").first()
        material2 = session.query(Material).filter_by(titulo="El Principito").first()

        copias = [
            Copia(
                id_material=material1.id_material,
                codigo_copia="CA001",
                ubicacion="Estante A",
                estado="disponible",
                coleccion="General"
            ),
            Copia(
                id_material=material2.id_material,
                codigo_copia="PR001",
                ubicacion="Estante B",
                estado="disponible",
                coleccion="Infantil"
            )
        ]

        session.add_all(copias)
        print("✔ Copias insertadas")

    session.commit()
    session.close()

    print("\n Seed completado correctamente\n")

if __name__ == "__main__":
    seed_database()

