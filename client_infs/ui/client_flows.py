"""
Flujos de interfaz de usuario para gestión de clientes.
"""

import click

from client_infs.services.client_service import ClientService
from client_infs.utils.ui_helpers import show_header, show_separator


def create_client_flow(environment: str):
    """Flujo para crear un cliente en el entorno especificado."""
    show_header(f"Crear Cliente - Entorno {environment.title()}")
    
    client_service = ClientService(environment)
    
    try:
        # Solicitar ID del cliente
        client_id = click.prompt("Ingrese el ID del cliente", type=str)
        
        show_separator()
        click.echo(f"🔑 Obteniendo token de acceso para {environment}...")
        access_token = client_service.get_access_token()
        click.echo("✓ Token obtenido exitosamente")
        
        # Crear datos del cliente con configuración estándar
        client_data = client_service.get_default_client_data(client_id)
        
        show_separator()
        # Mostrar datos del cliente a crear
        click.echo(f"👥 Cliente ID: {client_id}")
        click.echo(f"🌐 Entorno: {environment}")
        click.echo("⚙️  Configuración estándar:")
        click.echo(f"   • Client Secret: infosis")
        click.echo(f"   • Access Token Validity: 30000s")
        click.echo(f"   • Refresh Token Validity: 36000s")
        click.echo(f"   • Authorities: ANONYMOUS,USER,ADMIN")
        
        show_separator()
        if click.confirm("¿Proceder con la creación del cliente?"):
            click.echo("🚀 Creando cliente...")
            result = client_service.create_client(client_data, access_token)
            show_separator()
            click.echo("✅ Cliente creado exitosamente")
            click.echo(f"🆔 Cliente ID: {client_id}")
        else:
            click.echo("❌ Operación cancelada")
            
    except Exception as e:
        show_separator()
        click.echo(f"❌ Error: {e}", err=True)