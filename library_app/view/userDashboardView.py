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
