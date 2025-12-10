
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
