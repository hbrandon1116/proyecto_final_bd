# app.py
import tkinter as tk
from tkinter import ttk
from controllers import LibraryController
from views import PublicSearchView, LoginView, UserDashboard
import os
from dotenv import load_dotenv

load_dotenv("config_example.env")

DB_URL = os.getenv("DB_URL")  # ej: postgresql+psycopg2://user:pass@localhost:5432/biblioteca

def main():
    controller = LibraryController(DB_URL)
    controller.init_db()  # crea tablas (si es necesario)

    root = tk.Tk()
    root.title("Catálogo Biblioteca - Demo")

    nb = ttk.Notebook(root)
    nb.pack(fill='both', expand=True)

    public_tab = PublicSearchView(nb, controller)
    nb.add(public_tab, text="Consulta pública")

    # Login tab
    def on_login(user):
        # crear nueva pestaña con dashboard del usuario
        dash = UserDashboard(nb, controller, user)
        nb.add(dash, text=f"Usuario: {user.nombre}")
        nb.select(dash)

    login_tab = LoginView(nb, controller, on_login)
    nb.add(login_tab, text="Iniciar sesión")

    root.geometry("900x600")
    root.mainloop()

if __name__ == "__main__":
    main()
