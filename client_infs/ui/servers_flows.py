import re
import click

from InquirerPy import inquirer
from client_infs.utils.ui_helpers import show_header
from client_infs.config.settings import settings
from client_infs.services.server_service import ServerService

def server_flow():
    service = ServerService()

    actions = {
        "connect": service.connect_to_server,
        "restart": service.restart_server,
        "show_info": service.show_server_info
    }

    while True:
        choice = server_menu_view()

        if choice == "back":
            break
            
        server = server_list_view(service)

        if server == "back":
            break

        if choice not in actions:
            click.pause(f"❌ Opción no válida: {choice}")

        actions[choice](server)

        click.pause("...")


def server_menu_view():
    """Muestra el menú de gestión de servidores."""
    show_header("Gestión de Servidores")
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


def server_list_view(service: ServerService):
    show_header("Lista de Servidores")

    return inquirer.select(
        message="Seleccione un servidor:",
        choices=service.get_name_servers(),
        vi_mode=True
    ).execute()