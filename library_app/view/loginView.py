import tkinter as tk
from tkinter import messagebox

class LoginView(tk.Frame):
    def __init__(self, parent, controller, on_login_success, on_open_register):
        super().__init__(parent) 

        self.controller = controller
        self.on_login_success = on_login_success
        self.on_open_register = on_open_register


        tk.Label(self, text="Usuario").pack()
        self.username = tk.Entry(self)
        self.username.pack()

        tk.Label(self, text="Contraseña").pack()
        self.password = tk.Entry(self, show="*")
        self.password.pack()

        tk.Button(self, text="Ingresar", command=self.login).pack(pady=8)
        tk.Button(self, text="Registrar usuario", command=self.on_open_register).pack()
    def login(self):
        user = self.username.get()
        pwd = self.password.get()

        ok = self.controller.login(user, pwd)
        if ok:
            messagebox.showinfo("Éxito", "Inicio de sesión correcto.")
            self.on_login_success()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
