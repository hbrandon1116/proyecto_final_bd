import flet as ft
from model.models import Copia, Material,Estado
from sqlalchemy.orm import Session

class CopiaView(ft.Column):

    def __init__(self, session: Session, page: ft.Page):
        super().__init__()
        self.session = session
        self.page = page


         # ---- Controles UI ----

         
        self.search_field = ft.TextField(
            hint_text="Buscar por título...",
            #on_change=self.search_materials,
            expand=True
        )
        

        self.add_btn = ft.ElevatedButton(
            "Nuevo Material",
            icon=ft.Icons.ADD,
            on_click=self.open_create_dialog
        )

        # Tabla
        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Código")),
                ft.DataColumn(ft.Text("Material")),
                ft.DataColumn(ft.Text("ISBN")),
                ft.DataColumn(ft.Text("Estado")),
                ft.DataColumn(ft.Text("Colección")),
                ft.DataColumn(ft.Text("Ubicación")),
                ft.DataColumn(ft.Text("Formato")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=[],
            expand=True

        )

        self.controls = [
            ft.Row([self.search_field, self.add_btn]),
            ft.Container(self.table, expand=True)
        ]

        self.load_data()

  

    # ----------------------------
    # Cargar tabla
    # ----------------------------
    def load_data(self):
        self.table.rows.clear()

        copias = self.session.query(Copia).all()

        for c in copias:
            self.table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(c.id_copia))),
                        ft.DataCell(ft.Text(c.codigo_copia)),
                        ft.DataCell(ft.Text(c.material.titulo if c.material else "")),
                        ft.DataCell(ft.Text(c.material.isbn if c.material else "")),
                        ft.DataCell(ft.Text(c.estado_rel.nombre if c.estado_rel else "")),
                        ft.DataCell(ft.Text(c.coleccion or "")),
                        ft.DataCell(ft.Text(c.ubicacion or "")),
                        ft.DataCell(ft.Text(c.formato)),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(ft.Icons.EDIT, on_click=lambda _, cid=c.id_copia: self.open_edit_dialog(cid)),
                                ft.IconButton(ft.Icons.DELETE, on_click=lambda _: self.delete_item(c)),
                            ])
                        ),
                    ]
                )
            )

        self.page.update()

    # ----------------------------
    # Crear copia
    # ----------------------------
    def open_create_dialog(self, e):
        materiales = self.session.query(Material).all()

        material_dd = ft.Dropdown(
            label="Material",
            options=[
                ft.dropdown.Option(str(m.id_material), f"{m.titulo} — {m.isbn}")
                for m in materiales
            ],
            width=300
        )

        codigo = ft.TextField(label="Código de copia")
        ubicacion = ft.TextField(label="Ubicación")
        coleccion = ft.TextField(label="Colección")

        estado_all = self.session.query(Estado).order_by(Estado.nombre).all()

        estado = ft.Dropdown(
            label="Estado",
            width=300,
            options=[
                ft.dropdown.Option(str(e.id_estado), e.nombre)
                for e in estado_all
            ]
        )

        formato = ft.Dropdown(
            label="Formato",   
            width=300,
            options=[
                ft.dropdown.Option("fisico"),
                ft.dropdown.Option("digital"),
            ]
         
        )

        dialog = ft.AlertDialog(
            title=ft.Text("Crear copia"),
            content=ft.Column([
                material_dd,
                codigo,
                ubicacion,
                coleccion,
                estado,
                formato,
            ]),
            actions=[
                ft.ElevatedButton("Guardar"),
                ft.TextButton("Cancelar", on_click=lambda _: self.close_dialog(dialog))
            ]
        )

        def save(_):
            nueva = Copia(
                id_material=int(material_dd.value),
                codigo_copia=codigo.value,
                ubicacion=ubicacion.value,
                coleccion=coleccion.value,
                id_estado=int(estado.value),
                formato=formato.value,
            )
            self.session.add(nueva)
            self.session.commit()
            dialog.open = False
            self.load_data()
            self.page.update()
        
        dialog.actions[0].on_click = save
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()



    def close_dialog(self, dialog):
        dialog.open = False
        self.page.update()

    # ----------------------------
    # Editar copia
    # ----------------------------
    def open_edit_dialog(self, copia_id):
        copia = self.session.query(Copia).filter_by(id_copia=copia_id).first()
        if not copia:
            return

        materiales = self.session.query(Material).all()

        material_dd = ft.Dropdown(
            label="Material",
            value=str(copia.id_material),
            options=[
                ft.dropdown.Option(str(m.id_material), f"{m.titulo} — {m.isbn}")
                for m in materiales
            ],
            width=300
        )

        codigo = ft.TextField(label="Código de copia", value=copia.codigo_copia)
        ubicacion = ft.TextField(label="Ubicación", value=copia.ubicacion or "")
        coleccion = ft.TextField(label="Colección", value=copia.coleccion or "")

        estado_all = self.session.query(Estado).order_by(Estado.nombre).all()

        estado = ft.Dropdown(
            label="Estado",
            value=str(copia.id_estado),
            width=300,
            options=[
                ft.dropdown.Option(str(e.id_estado), e.nombre)
                for e in estado_all
            ]
        )

        formato = ft.Dropdown(
            label="Formato",
            value=copia.formato,
            width=300,
            options=[
                ft.dropdown.Option("fisico"),
                ft.dropdown.Option("digital"),
            ]
        )

        dialog = ft.AlertDialog(
            title=ft.Text("Editar copia"),
            content=ft.Column([
                material_dd,
                codigo,
                ubicacion,
                coleccion,
                estado,
                formato,
            ]),
            actions=[
                ft.ElevatedButton("Guardar cambios"),
                ft.TextButton("Cancelar", on_click=lambda _: self.close_dialog(dialog))
            ]
        )

        def save(_):
            copia.id_material = int(material_dd.value)
            copia.codigo_copia = codigo.value
            copia.ubicacion = ubicacion.value
            copia.coleccion = coleccion.value
            copia.id_estado = int(estado.value)
            copia.formato = formato.value

            self.session.commit()
            dialog.open = False
            self.load_data()
            self.page.update()
        
        dialog.actions[0].on_click = save
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.open(dialog)

    def delete_item(self, copia):
        self.session.delete(copia)
        self.session.commit()
        self.load_data()