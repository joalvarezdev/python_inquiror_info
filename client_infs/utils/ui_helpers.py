"""
Utilidades para mejorar la interfaz de usuario.
"""

import os
import click


def clear_screen():
    """Limpia la pantalla de la terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')


def show_header(title: str = "INFOSIS CLI"):
    """Limpia la pantalla sin mostrar header."""
    clear_screen()


def show_separator():
    """Muestra un separador visual."""
    click.echo()
    click.echo("-" * 60)
    click.echo()