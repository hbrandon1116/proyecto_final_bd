

class RegisterView:
    def __init__(self, root, controller, on_register_success, on_back):
        self.root = root
        self.controller = controller
        self.on_register_success = on_register_success
        self.on_back = on_back

        root.title("Registrar Usuario")

        tk.Label(root, text="Nuevo Usuario").pack()
        self.username = tk.Entry(root)
        self.username.pack()

        tk.Label(root, text="Contraseña").pack()
        self.password = tk.Entry(root, show="*")
        self.password.pack()

        tk.Button(root, text="Crear usuario", command=self.register).pack(pady=8)
        tk.Button(root, text="Volver", command=self.on_back).pack()

    def register(self):
        user = self.username.get()
        pwd = self.password.get()

        ok = self.controller.register(user, pwd)
        if ok:
            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
            self.on_register_success()
        else:
            messagebox.showerror("Error", "El usuario ya existe.")