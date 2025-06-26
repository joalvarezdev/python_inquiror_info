import re

from InquirerPy import inquirer
from client_infs.utils.ui_helpers import show_header
from client_infs.config.settings import settings

def server_flow():
    service = None

    while True:
        choice = server_menu_view()

        server = server_list_view()

        if choice == "back":
            break
        elif choice == "connect":
            # Aquí se llamaría a la función para conectar al servidor
            print("Conectando al servidor...")
            # service.connect_to_server()
        elif choice == "restart":
            # Aquí se llamaría a la función para reiniciar el servidor
            print("Reiniciando el servidor...")
            # service.restart_server()
        elif choice == "show_info":
            # Aquí se mostrarían las credenciales del servidor
            print("Mostrando credenciales del servidor...")
            # service.show_server_info()


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


def server_list_view():
    show_header("Lista de Servidores")

    servers = []
    with open(settings.server_file, "r") as file:
        content = file.read()

    names = re.findall(r'\[([^\]]+)\]', content)

    for name in names:
        servers.append({"name": name, "value": name})

    servers.append({"name": "← Volver al menú de gestión", "value": "back"})


    return inquirer.select(
        message="Seleccione un servidor:",
        choices=servers,
        vi_mode=True
    ).execute()