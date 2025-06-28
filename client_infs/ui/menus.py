"""
Menús de la interfaz de usuario.
"""

from InquirerPy import inquirer
from client_infs.utils.ui_helpers import show_header


def show_main_menu():
    """Muestra el menú principal con navegación vim (hjkl)."""
    show_header()
    return inquirer.select(
        message="Seleccione una opción:",
        choices=[
            {"name": "👥 Crear cliente", "value": "create_client"},
            {"name": "🕐 Quick Pass (Fichaje)", "value": "quick_pass"},
            {"name": "🖥️  Servidores", "value": "servers"},
            {"name": "🚪 Salir", "value": "exit"}
        ],
        vi_mode=True
    ).execute()

