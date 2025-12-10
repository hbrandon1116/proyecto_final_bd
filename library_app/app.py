from dotenv import load_dotenv
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from controllers.authControllers import AuthController
from view.views import MainView
from view.loginView import LoginView
from view.registerView import RegisterView
from sqlalchemy.orm import sessionmaker
from model.db import engine



def main():

    # ---------------------------
    # Crear ventana principal
    # ---------------------------
    root = tk.Tk()
    root.title("Biblioteca App")
    root.geometry("900x600")

    # Notebook (tabs)
    nb = ttk.Notebook(root)
    nb.pack(fill="both", expand=True)

    # ---------------------------
    # Configurar SQLAlchemy
    # ---------------------------
    Session = sessionmaker(bind=engine)
    session = Session()

    # Controlador de autenticación
    auth_controller = AuthController(session)

    # ---------------------------
    # Callback: después del login
    # ---------------------------
    def on_login_success():
        # Limpiar notebook
        for tab in nb.tabs():
            nb.forget(tab)

        main_view = MainView(root, auth_controller, on_logout)
        nb.add(main_view, text="Inicio")

    # ---------------------------
    # Callback: después del logout
    # ---------------------------
    
    def on_register_success():
        messagebox.showinfo("Éxito", "Ahora puedes iniciar sesión.")
        on_back_to_login()

    def on_back_to_login():
        for tab in nb.tabs():
            nb.forget(tab)
        login_view = LoginView(nb, auth_controller, on_login_success, on_open_register)
        nb.add(login_view, text="Iniciar sesión")

    def on_open_register():
    # Limpiar tabs
        for tab in nb.tabs():
            nb.forget(tab)

        register_view = RegisterView(
            nb,
        auth_controller,
            on_register_success,
            on_back_to_login
        )
        nb.add(register_view, text="Registrar")


    def on_logout():
        # Limpiar notebook
        for tab in nb.tabs():
            nb.forget(tab)

        login_view = LoginView(nb, auth_controller, on_login_success)
        nb.add(login_view, text="Iniciar sesión")

    # ---------------------------
    # Mostrar vista inicial (Login)
    # ---------------------------
    login_view = LoginView(nb, auth_controller, on_login_success, on_open_register)
    nb.add(login_view, text="Iniciar sesión")

    root.mainloop()


if __name__ == "__main__":
    main()
