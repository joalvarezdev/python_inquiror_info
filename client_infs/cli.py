#!/usr/bin/env python3
"""
Interfaz de línea de comandos principal.
"""

import click

from .ui.menus import show_main_menu
from .ui.client_flows import client_flows
from .ui.quick_pass_flows import quick_pass_flow
from .ui.servers_flows import server_flow


def main():
    """Función principal con menús interactivos."""

    
    # Diccionario de acciones para el menú principal
    actions = {
        "create_client": client_flows,
        "quick_pass": quick_pass_flow,
        "servers": server_flow
    }
    
    try:
        while True:
            choice = show_main_menu()
            
            if choice == "exit":
                break

            actions.get(choice, lambda: click.echo("Opción no válida"))()
                        
    except (KeyboardInterrupt, EOFError):
        click.echo("\n¡Hasta luego!")


if __name__ == "__main__":
    main()