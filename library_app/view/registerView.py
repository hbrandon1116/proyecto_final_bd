import tkinter as tk
from tkinter import ttk, messagebox 

class RegisterView(tk.Frame):
    def __init__(self, parent, controller, on_register_success, on_back):
        super().__init__(parent)   # <-- AHORA ES UN FRAME

        self.controller = controller
        self.on_register_success = on_register_success
        self.on_back = on_back


        tk.Label(self, text="Nuevo Usuario").pack()
        self.username = tk.Entry(self)
        self.username.pack()

        tk.Label(self, text="Contraseña").pack()
        self.password = tk.Entry(self, show="*")
        self.password.pack()

        tk.Label(self, text="Correo").pack()
        self.email = tk.Entry(self)
        self.email.pack()

        tk.Label(self, text="Tipo de usuario (estudiante/empleado)").pack()
        self.user_type = tk.Entry(self)
        self.user_type.pack()


        tk.Button(self, text="Crear usuario", command=self.register).pack(pady=8)
        tk.Button(self, text="Volver", command=self.on_back).pack()

        
    def register(self):
        
        user = self.username.get()
        pwd = self.password.get()
        email = self.email.get()
        user_type = self.user_type.get()
        ok = self.controller.register(user, email, pwd, user_type)
        if ok:
            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
            self.on_register_success()
        else:
            messagebox.showerror("Error", "El usuario ya existe.")