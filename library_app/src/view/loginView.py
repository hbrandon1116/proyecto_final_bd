import flet as ft

class LoginView(ft.View):
    def __init__(self, page, controller, on_login_success, on_open_register):
        super().__init__(route="/login")

        self.page = page
        self.controller = controller
        self.on_login_success = on_login_success
        self.on_open_register = on_open_register

        # Campos del formulario
        self.username = ft.TextField(label="Usuario", width=300)
        self.password = ft.TextField(label="Contraseña", password=True, width=300)

        # Botones
        login_btn = ft.ElevatedButton("Ingresar", on_click=self.login)
        register_btn = ft.TextButton("Registrar usuario", on_click=lambda _: self.on_open_register())

        # Layout
        self.controls = [
            ft.Column(
                [
                    ft.Text("Inicio de sesión", size=22, weight="bold"),
                    self.username,
                    self.password,
                    login_btn,
                    register_btn
                ],
                alignment="center",
                horizontal_alignment="center",
                spacing=15
            )
        ]

    # ---------------------------
    # Lógica del login
    # ---------------------------
    def login(self, _):
        user = self.username.value
        pwd = self.password.value

        ok = self.controller.login(user, pwd)

        if ok:
            # Notificación tipo SnackBar
            self.page.snack_bar = ft.SnackBar(
                ft.Text("Inicio de sesión correcto."),
            )
            self.page.snack_bar.open = True
            self.page.update()
            self.on_login_success()

        else:
            self.page.snack_bar = ft.SnackBar(
                ft.Text("Usuario o contraseña incorrectos."),
                bgcolor="red"
            )
            self.page.snack_bar.open = True
            self.page.update()
