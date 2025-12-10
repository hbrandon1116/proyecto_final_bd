import flet as ft
from dotenv import load_dotenv
from controllers.authControllers import AuthController
from view.views import MainView
from view.loginView import LoginView
from view.registerView import RegisterView
from sqlalchemy.orm import sessionmaker
from model.db import engine


def main(page: ft.Page):

    # Configuración de la ventana principal
    page.title = "Biblioteca App"
    page.window_width = 900
    page.window_height = 600
    page.horizontal_alignment = "center"
    page.scroll = "auto"

    # SQLAlchemy
    Session = sessionmaker(bind=engine)
    session = Session()

    auth_controller = AuthController(session)

    # ----------- Navegación -----------

    def go_to(view_name):
        page.views.clear()

        if view_name == "login":
            page.views.append(
                LoginView(
                    page,
                    auth_controller,
                    on_login_success,
                    on_open_register
                )
            )

        elif view_name == "register":
            page.views.append(
                RegisterView(
                    page,
                    auth_controller,
                    on_register_success,
                    on_back_to_login
                )
            )

        elif view_name == "home":
            page.views.append(
                MainView(
                    page,
                    auth_controller,
                    on_logout
                )
            )

        page.update()

    # ----------- Callbacks -----------

    def on_login_success():
        go_to("home")

    def on_logout():
        go_to("login")

    def on_register_success():
        page.snack_bar = ft.SnackBar(
            ft.Text("Registro exitoso. Ahora puedes iniciar sesión.")
        )
        page.snack_bar.open = True
        page.update()
        go_to("login")

    def on_open_register():
        go_to("register")

    def on_back_to_login():
        go_to("login")

    # ----------- Vista inicial -----------

    go_to("login")


# Lanzar app Flet
if __name__ == "__main__":
    ft.app(target=main)
