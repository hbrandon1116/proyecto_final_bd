# views.py
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.controllers import LibraryController
from functools import partial
from model.models import Copia
import os

class PublicSearchView(ttk.Frame):
    def __init__(self, parent, controller: LibraryController):
        super().__init__(parent)
        self.controller = controller
        self.build_ui()

    def build_ui(self):
        # Search fields
        frm = ttk.Frame(self)
        frm.pack(fill='x', padx=8, pady=8)

        ttk.Label(frm, text="Buscar (título/descripcion):").grid(row=0, column=0, sticky='w')
        self.q_entry = ttk.Entry(frm, width=40)
        self.q_entry.grid(row=0, column=1, sticky='w')

        ttk.Label(frm, text="Colección:").grid(row=1, column=0, sticky='w')
        self.coleccion_entry =ttk.Entry(frm)
        self.coleccion_entry.grid(row=1, column=1, sticky='w')

        ttk.Button(frm, text="Buscar disponibles", command=self.on_search).grid(row=0, column=2, rowspan=2, padx=6)

        # Result table
        self.tree = ttk.Treeview(self, columns=("codigo","titulo","coleccion","estado"), show='headings')
        for c in ("codigo","titulo","coleccion","estado"):
            self.tree.heading(c, text=c.title())
            self.tree.column(c, width=150)
        self.tree.pack(fill='both', expand=True, padx=8, pady=8)
        self.tree.bind("<Double-1>", self.on_double_click)

    def on_search(self):
        q = self.q_entry.get().strip() or None
        col = self.coleccion_entry.get().strip() or None
        rows = self.controller.search_public(q_text=q, coleccion=col, estado='disponible')
        # limpiar
        for r in self.tree.get_children():
            self.tree.delete(r)
        for c in rows:
            titulo = c.material.titulo if c.material else ""
            self.tree.insert('', 'end', iid=str(c.id_copia), values=(c.codigo_copia or '', titulo, c.coleccion or '', c.estado or ''))

    def on_double_click(self, event):
        
        iid = self.tree.focus()
        if not iid:
            return
        c_id = int(iid)
        copia = self.controller.session.get(self.controller.session.get_bind().mapper_registry._class_registry['Copia'], c_id) \
            if False else self.controller.session.get(type(self.controller.session.get(Copia, c_id)), c_id)
        # Simpler: fetch via session
        copia = self.controller.session.get(self.controller.session.get_bind().engine.table_names and None or None, c_id) if False else None
        
        copia = self.controller.session.get(Copia, c_id)
        if not copia: return
        titulo = copia.material.titulo if copia.material else ""
        info = f"ID copia: {copia.id_copia}\nCódigo: {copia.codigo_copia}\nTítulo: {titulo}\nUbicación: {copia.ubicacion}\nColección: {copia.coleccion}\nEstado: {copia.estado}\nFormato: {copia.formato}\nFecha adquisición: {copia.fecha_adquisicion}"
        messagebox.showinfo("Detalle recurso", info)

class LoginView(ttk.Frame):
    def __init__(self, parent, controller: LibraryController, on_login):
        super().__init__(parent)
        self.controller = controller
        self.on_login = on_login
        self.build_ui()

    def build_ui(self):
        frm = ttk.Frame(self)
        frm.pack(padx=20, pady=20)
        ttk.Label(frm, text="Correo:").grid(row=0, column=0, sticky='w')
        self.email = ttk.Entry(frm, width=40); self.email.grid(row=0, column=1)
        ttk.Label(frm, text="(contraseña simulada)").grid(row=1, column=0, columnspan=2, sticky='w')
        ttk.Button(frm, text="Iniciar sesión", command=self.try_login).grid(row=2, column=0, columnspan=2, pady=8)

    def try_login(self):
        correo = self.email.get().strip()
        user = self.controller.find_user_by_email(correo)
        if not user:
            messagebox.showerror("Error", "Usuario no encontrado")
            return
        # No se valida contraseña en esta demo; suponer login correcto
        self.on_login(user)

class UserDashboard(ttk.Frame):
    def __init__(self, parent, controller: LibraryController, user):
        super().__init__(parent)
        self.controller = controller
        self.user = user
        self.build_ui()

    def build_ui(self):
        ttk.Label(self, text=f"Conectado como: {self.user.nombre} ({self.user.tipo_usuario})").pack(anchor='w', padx=8, pady=4)
        tabs = ttk.Notebook(self)
        tabs.pack(fill='both', expand=True)

        # Prestamos
        self.tab_prest = ttk.Frame(tabs); tabs.add(self.tab_prest, text="Prestados")
        self.tree_pre = ttk.Treeview(self.tab_prest, columns=("id","titulo","fecha","estado","multa"), show='headings')
        for c in ("id","titulo","fecha","estado","multa"):
            self.tree_pre.heading(c, text=c.title())
        self.tree_pre.pack(fill='both', expand=True, padx=8, pady=8)

        # Reservas
        self.tab_res = ttk.Frame(tabs); tabs.add(self.tab_res, text="Reservas")
        self.tree_res = ttk.Treeview(self.tab_res, columns=("id","titulo","fecha","estado"), show='headings')
        for c in ("id","titulo","fecha","estado"):
            self.tree_res.heading(c, text=c.title())
        self.tree_res.pack(fill='both', expand=True, padx=8, pady=8)

        # Multas
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill='x', padx=8, pady=4)
        ttk.Button(btn_frame, text="Refrescar", command=self.load_all).pack(side='left')
        ttk.Button(btn_frame, text="Pagar multa (fila seleccionada)", command=self.pay_selected).pack(side='left', padx=6)

        self.load_all()

    def load_all(self):
        prestamos = self.controller.get_prestamos_by_user(self.user.id_usuario)
        for r in self.tree_pre.get_children(): self.tree_pre.delete(r)
        for p in prestamos:
            titulo = p.copia.material.titulo if p.copia and p.copia.material else ""
            self.tree_pre.insert('', 'end', iid=str(p.id_prestamo), values=(p.id_prestamo, titulo, p.fecha_prestamo, p.estado, float(p.multa or 0)))

        reservas = self.controller.get_reservas_by_user(self.user.id_usuario)
        for r in self.tree_res.get_children(): self.tree_res.delete(r)
        for res in reservas:
            titulo = res.copia.material.titulo if res.copia and res.copia.material else ""
            self.tree_res.insert('', 'end', iid=str(res.id_reserva), values=(res.id_reserva, titulo, res.fecha_reserva, res.estado))

    def pay_selected(self):
        sel = self.tree_pre.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecciona un préstamo con multa")
            return
        pid = int(sel[0])
        success = self.controller.pay_multa(pid)
        if success:
            messagebox.showinfo("Pago", "Pago simulado realizado. Multa puesta a 0.")
            self.load_all()
        else:
            messagebox.showerror("Error", "No se pudo procesar el pago")

class LoginView:
    def __init__(self, root, controller, on_login_success, on_open_register):
        self.root = root
        self.controller = controller
        self.on_login_success = on_login_success
        self.on_open_register = on_open_register

        root.title("Iniciar Sesión")

        tk.Label(root, text="Usuario").pack()
        self.username = tk.Entry(root)
        self.username.pack()

        tk.Label(root, text="Contraseña").pack()
        self.password = tk.Entry(root, show="*")
        self.password.pack()

        tk.Button(root, text="Ingresar", command=self.login).pack(pady=8)
        tk.Button(root, text="Registrar usuario", command=self.on_open_register).pack()

    def login(self):
        user = self.username.get()
        pwd = self.password.get()

        ok = self.controller.login(user, pwd)
        if ok:
            messagebox.showinfo("Éxito", "Inicio de sesión correcto.")
            self.on_login_success()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")


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