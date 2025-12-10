# views.py
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.authControllers import AuthController


class MainView:
    def __init__(self, root, auth_controller, on_logout):
        self.root = root
        self.auth_controller = auth_controller
        self.on_logout = on_logout

        # 🔥 Frame que contiene esta vista
        self.frame = tk.Frame(root)
        self.frame.pack(fill="both", expand=True)

        tk.Label(
            self.frame,
            text=f"Bienvenido {auth_controller.current_user.nombre}"
        ).pack()

        tk.Button(
            self.frame,
            text="Cerrar sesión",
            command=self.logout
        ).pack(pady=10)

    def logout(self):
        self.frame.destroy()
        self.auth_controller.logout()
        self.on_logout()