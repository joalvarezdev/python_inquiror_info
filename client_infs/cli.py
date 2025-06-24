#!/usr/bin/env python3
"""
Interfaz de línea de comandos principal.
"""

import click

from .ui.menus import show_main_menu, show_environment_menu
from .ui.client_flows import create_client_flow
from .ui.quick_pass_flows import quick_pass_flow


def main():
    """Función principal con menús interactivos."""
    
    try:
        while True:
            # Menú principal
            main_choice = show_main_menu()
            
            if main_choice == "exit":
                click.echo("¡Hasta luego!")
                break
            elif main_choice == "create_client":
                # Submenú de entornos
                while True:
                    env_choice = show_environment_menu()
                    
                    if env_choice == "back":
                        break
                    elif env_choice == "testing":
                        create_client_flow("testing")
                        click.pause("Presione Enter para continuar...")
                    elif env_choice == "production":
                        click.echo("\n⚠️  Funcionalidad de producción en desarrollo")
                        click.echo("Esta opción estará disponible próximamente.")
                        click.pause("Presione Enter para continuar...")
            elif main_choice == "quick_pass":
                # Submenu de Quick Pass
                quick_pass_flow()
                        
    except (KeyboardInterrupt, EOFError):
        click.echo("\n¡Hasta luego!")


if __name__ == "__main__":
    main()