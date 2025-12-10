
import tkinter as tk
from tkinter import ttk
from controllers.controllers import LibraryController
from view.views import PublicSearchView, LoginView, UserDashboard
import os
from dotenv import load_dotenv

load_dotenv("config_example.env")

DB_URL = os.getenv("DB_URL")  
def main():
    controller = LibraryController(DB_URL)
    controller.init_db() 

    root = tk.Tk()
    root.title("Catálogo Biblioteca")

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
"""
import tkinter as tk
from controllers.auth_controller import AuthController
from view.auth_views import LoginView, RegisterView, MainView


class App:
    def __init__(self, root):
        self.root = root
        self.auth_controller = AuthController()

        self.show_login()

    # ------------------------
    #  VISTAS
    # ------------------------

    def show_login(self):
        self.clear_window()
        LoginView(
            root=self.root,
            controller=self.auth_controller,
            on_login_success=self.show_main,
            on_open_register=self.show_register
        )

    def show_register(self):
        self.clear_window()
        RegisterView(
            root=self.root,
            controller=self.auth_controller,
            on_register_success=self.show_login,
            on_back=self.show_login
        )

    def show_main(self):
        self.clear_window()
        MainView(
            root=self.root,
            auth_controller=self.auth_controller,
            on_logout=self.show_login
        )

    # ------------------------
    #  Limpiar ventana
    # ------------------------
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
"""