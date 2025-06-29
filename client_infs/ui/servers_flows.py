import click
import sys

from InquirerPy import inquirer
from client_infs.utils.ui_helpers import show_header
from client_infs.services.server_service import ServerService

def server_flow():

    actions = {
        "connect": connect,
        "restart": restart,
        "show_info": show_info
    }

    while True:
        choice = server_menu_view()

        if choice == "back":
            break
            
        server = server_list_view()

        if server == "back":
            break

        if choice not in actions:
            click.pause(f"❌ Opción no válida: {choice}")

        actions.get(choice, lambda: click.echo("Opción no válida"))(server)

        click.pause("...")


def connect(server: str = ""):
    console = __is_console()

    ServerService().connect_to_server(server) if len(server) != 0 else ServerService().connect_to_server(console)


def restart(server: str = ""):
    console = __is_console()
    ServerService().restart_server(server) if len(server) != 0 else ServerService().restart_server(console)


def show_info(server: str = ""):
    console = __is_console()
    ServerService().show_server_info(server) if len(server) != 0 else ServerService().show_server_info(console)


def server_menu_view():
    """Muestra el menú de gestión de servidores."""
    show_header()
    return inquirer.select(
        message="Seleccione una opción:",
        choices=[
            {"name": "🌐 Ingresar a un servidor", "value": "connect"},
            {"name": "🔄 Reiniciar servidor", "value": "restart"},
            {"name": "🔑 Mostrar credenciales", "value": "show_info"},
            {"name": "← Volver al menú principal", "value": "back"}
        ],
        vi_mode=True
    ).execute()


def server_list_view():
    show_header()

    return inquirer.select(
        message="Seleccione un servidor:",
        choices=ServerService().get_name_servers(),
        vi_mode=True
    ).execute()


def __is_console() -> str:
    return sys.argv[1].upper() if len(sys.argv) > 1 else ""