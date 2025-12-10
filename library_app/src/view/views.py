import flet as ft

class MainView(ft.View):
    def __init__(self, page, auth_controller, on_logout):
        super().__init__(route="/home")

        self.page = page
        self.auth_controller = auth_controller
        self.on_logout = on_logout

        welcome_text = ft.Text(
            f"Bienvenido {auth_controller.current_user.nombre}",
            size=22,
            weight="bold"
        )

        logout_btn = ft.ElevatedButton(
            "Cerrar sesión",
            on_click=self.logout,
            bgcolor="red",
            color="white"
        )

        self.controls = [
            ft.Column(
                [
                    welcome_text,
                    logout_btn,
                ],
                alignment="center",
                horizontal_alignment="center",
                spacing=20
            )
        ]

    # ---------------------------
    # Cerrar sesión
    # ---------------------------
    def logout(self, _):
        self.auth_controller.logout()

        self.page.snack_bar = ft.SnackBar(
            ft.Text("Sesión cerrada."),
        )
        self.page.snack_bar.open = True
        self.page.update()

        self.on_logout()
