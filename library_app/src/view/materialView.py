import flet as ft
from sqlalchemy.orm import Session
from model.models import Material, Autor, MaterialAutor, Idioma


class MaterialView(ft.Column):
    def __init__(self, session: Session, page: ft.Page):
        super().__init__()
        self.session = session
        self.page = page

        # ---- Controles UI ----
        self.search_field = ft.TextField(
            hint_text="Buscar por título...",
            on_change=self.search_materials,
            expand=True
        )

        self.add_btn = ft.ElevatedButton(
            "Nuevo Material",
            icon=ft.Icons.ADD,
            on_click=self.open_create_modal
        )

        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Título")),
                ft.DataColumn(ft.Text("Idioma")),
                ft.DataColumn(ft.Text("Año")),
                ft.DataColumn(ft.Text("Autores")),
            ],
            rows=[],
            expand=True
        )

        self.controls = [
            ft.Row([self.search_field, self.add_btn]),
            ft.Container(self.table, expand=True)
        ]

        self.load_materials()

    # --------------------------------------------------------
    #                  CARGAR MATERIALES
    # --------------------------------------------------------
    def load_materials(self):
        materiales = self.session.query(Material).all()

        self.table.rows = []
        for m in materiales:
            autores = ", ".join([ma.autor.nombre for ma in m.autores])

            self.table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(m.id_material))),
                        ft.DataCell(ft.Text(m.titulo)),
                        ft.DataCell(ft.Text(m.id_idioma or "")),
                        ft.DataCell(ft.Text(str(m.año_publicacion or ""))),
                        ft.DataCell(ft.Text(autores)),
                    ],
                    on_select_changed=lambda e, mat=m: self.open_detail_modal(mat)
                )
            )
        self.page.update()

    # --------------------------------------------------------
    #                  BUSCAR MATERIALES
    # --------------------------------------------------------
    def search_materials(self, e):
        text = self.search_field.value.lower()

        query = (
            self.session.query(Material)
            .filter(Material.titulo.ilike(f"%{text}%"))
            .all()
        )

        self.table.rows = []
        for m in query:
            autores = ", ".join([ma.autor.nombre for ma in m.autores])
            self.table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(m.id_material))),
                        ft.DataCell(ft.Text(m.titulo)),
                        ft.DataCell(ft.Text(m.id_idioma or "")),
                        ft.DataCell(ft.Text(str(m.año_publicacion or ""))),
                        ft.DataCell(ft.Text(autores)),
                    ],
                    on_select_changed=lambda e, mat=m: self.open_detail_modal(mat)
                )
            )
        self.page.update()

    # --------------------------------------------------------
    #              MODAL PARA DETALLE + EDITAR + BORRAR
    # --------------------------------------------------------
    def open_detail_modal(self, material: Material):
        autores = ", ".join([ma.autor.nombre for ma in material.autores])

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Detalles del material"),
            content=ft.Column(
                [
                    ft.Text(f"Título: {material.titulo}"),
                    ft.Text(f"Idioma ID: {material.id_idioma}"),
                    ft.Text(f"Año: {material.año_publicacion}"),
                    ft.Text(f"Descripción: {material.descripcion}"),
                    ft.Text(f"Autores: {autores}")
                ],
                scroll="auto",
            ),
            actions=[
                ft.TextButton("Editar", on_click=lambda _: self.edit_material(material, dialog)),
                ft.TextButton("Eliminar", on_click=lambda _: self.delete_material(material, dialog)),
                ft.TextButton("Cerrar", on_click=lambda _: self.close_dialog(dialog)),
            ]
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def close_dialog(self, dialog):
        dialog.open = False
        self.page.update()

    # --------------------------------------------------------
    #                    ELIMINAR MATERIAL
    # --------------------------------------------------------
    def delete_material(self, material, dialog):
        self.session.delete(material)
        self.session.commit()
        dialog.open = False
        self.load_materials()

    # --------------------------------------------------------
    #                    EDITAR MATERIAL
    # --------------------------------------------------------
    def edit_material(self, material, dialog):
        dialog.open = False

        titulo = ft.TextField(value=material.titulo)
        anio = ft.TextField(value=str(material.año_publicacion or ""))
        descripcion = ft.TextField(value=material.descripcion or "", multiline=True)

        save_btn = ft.ElevatedButton("Guardar cambios")

        edit_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Editar material"),
            content=ft.Column(
                [
                    titulo,
                    descripcion,
                    anio
                ],
                scroll="auto"
            ),
            actions=[
                save_btn,
                ft.TextButton("Cancelar", on_click=lambda _: self.close_dialog(edit_dialog))
            ]
        )

        def save_changes(e):
            material.titulo = titulo.value
            material.descripcion = descripcion.value
            material.año_publicacion = int(anio.value) if anio.value.isdigit() else None

            self.session.commit()
            edit_dialog.open = False
            self.load_materials()

        save_btn.on_click = save_changes

        self.page.dialog = edit_dialog
        edit_dialog.open = True
        self.page.update()

    # --------------------------------------------------------
    #             MODAL PARA CREAR NUEVO MATERIAL
    # --------------------------------------------------------
    def open_create_modal(self, e):
        titulo = ft.TextField(label="Título")
        descripcion = ft.TextField(label="Descripción", multiline=True)
        anio = ft.TextField(label="Año publicación")
        idioma = ft.TextField(label="ID idioma")

        create_btn = ft.ElevatedButton("Crear")

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Nuevo Material"),
            content=ft.Column([titulo, descripcion, anio, idioma], scroll="auto"),
            actions=[
                create_btn,
                ft.TextButton("Cancelar", on_click=lambda _: self.close_dialog(dialog))
            ]
        )

        def create_material(e):
            nuevo = Material(
                titulo=titulo.value,
                descripcion=descripcion.value,
                año_publicacion=int(anio.value) if anio.value.isdigit() else None,
                id_idioma=int(idioma.value) if idioma.value else None,
            )

            self.session.add(nuevo)
            self.session.commit()

            dialog.open = False
            self.load_materials()

        create_btn.on_click = create_material

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
