# views.py
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.authControllers import AuthController


class MainView:
    def __init__(self, root, auth_controller, on_logout):
        self.root = root
        self.auth_controller = auth_controller
        self.on_logout = on_logout

        root.title("Panel Principal")

        tk.Label(root, text=f"Bienvenido {auth_controller.current_user['username']}").pack()
        
        tk.Button(root, text="Cerrar sesión", command=self.logout).pack(pady=10)

    def logout(self):
        self.auth_controller.logout()
        self.on_logout()