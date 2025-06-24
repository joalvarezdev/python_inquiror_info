"""
Flujos de interfaz de usuario para Quick Pass.
"""

import os
import click
from InquirerPy import inquirer

from client_infs.services.quick_pass_service import QuickPassService
from client_infs.utils.ui_helpers import show_header, show_separator


def quick_pass_menu():
    """Muestra el menú de Quick Pass."""
    show_header("Quick Pass - Sistema de Fichaje")
    return inquirer.select(
        message="Seleccione una opción:",
        choices=[
            {"name": "🕐 Fichar (modo silencioso)", "value": "fichar"},
            {"name": "👁️  Fichar (ver navegador)", "value": "fichar_visible"},
            {"name": "📊 Ver logs recientes", "value": "logs"},
            {"name": "⚙️  Configurar credenciales", "value": "config"},
            {"name": "← Volver al menú principal", "value": "back"}
        ],
        vi_mode=True
    ).execute()


def quick_pass_flow():
    """Flujo principal de Quick Pass."""
    service = QuickPassService()
    
    while True:
        choice = quick_pass_menu()
        
        if choice == "back":
            break
        elif choice == "fichar":
            fichar_flow(service, headless=True)
        elif choice == "fichar_visible":
            fichar_flow(service, headless=False)
        elif choice == "logs":
            show_logs_flow(service)
        elif choice == "config":
            config_flow(service)
        
        if choice != "back":
            click.pause("Presione Enter para continuar...")


def fichar_flow(service: QuickPassService, headless: bool = True):
    """Flujo para realizar fichaje."""
    mode_text = "silencioso" if headless else "visible"
    show_header(f"Fichaje - Modo {mode_text.title()}")
    
    click.echo(f"🕐 Iniciando proceso de fichaje...")
    
    # Verificar configuración
    config = service.get_quick_pass_config()
    if not service.validate_config(config):
        click.echo("❌ Configuración incompleta.")
        show_separator()
        click.echo("Faltan las siguientes variables de entorno:")
        click.echo("• QUICK_PASS_URL: URL del sistema de fichaje")
        click.echo("• QUICK_PASS_INGRESS: Código de ingreso")
        click.echo("• QUICK_PASS_LEGAJO: Número de legajo")
        click.echo("• QUICK_PASS_PIN: PIN de acceso")
        show_separator()
        click.echo("💡 Usa la opción 'Configurar credenciales' para configurarlas.")
        return
    
    click.echo("✓ Configuración encontrada")
    if headless:
        click.echo("🤖 Ejecutando fichaje en segundo plano...")
    else:
        click.echo("🌐 Abriendo navegador...")
    
    show_separator()
    
    # Realizar fichaje
    try:
        result = service.perform_quick_pass(headless)
        
        show_separator()
        click.echo("RESULTADO DEL FICHAJE:")
        click.echo("="*50)
        click.echo(result)
        click.echo("="*50)
        
        if "correcto" in result.lower():
            show_separator()
            click.echo("✅ Fichaje realizado correctamente")
            click.echo("📋 Resultado copiado al portapapeles")
            click.echo("📁 Log guardado en registros")
        else:
            show_separator()
            click.echo("⚠️  Verificar resultado del fichaje")
            click.echo("💡 Si hay problemas, intenta con 'Fichar (ver navegador)' para debug")
            
    except Exception as e:
        show_separator()
        click.echo("❌ Error durante el fichaje:")
        click.echo(str(e))
        show_separator()
        click.echo("🔧 Pasos para solucionar:")
        click.echo("1. Verifica que Chrome/Chromium esté instalado")
        click.echo("2. Verifica que ChromeDriver esté instalado")
        click.echo("3. Verifica tu configuración QUICK_PASS_* en el .env")
        click.echo("4. Intenta con 'Fichar (ver navegador)' para ver qué pasa")


def show_logs_flow(service: QuickPassService):
    """Flujo para mostrar logs recientes."""
    show_header("Logs de Fichaje - Últimos 7 días")
    
    logs = service.get_recent_logs(7)
    
    if not logs:
        click.echo("📭 No hay logs recientes encontrados")
        show_separator()
        click.echo("💡 Los logs se guardan automáticamente cuando el fichaje es exitoso")
        return
    
    for i, log in enumerate(logs, 1):
        click.echo(f"{i:2d}. {log['date']} ({log['day']}) - {log['time']}")
        click.echo(f"    {log['status']}")
        if i < len(logs):
            click.echo()
    
    show_separator()
    click.echo(f"📈 Total de registros: {len(logs)}")


def config_flow(service: QuickPassService):
    """Flujo para configurar credenciales de Quick Pass."""
    show_header("Configuración de Quick Pass")
    
    config_file = service.config_dir / ".env"
    
    click.echo(f"📁 Archivo de configuración: {config_file}")
    show_separator()
    
    click.echo("💡 Agrega estas variables a tu archivo .env:")
    click.echo()
    
    # Mostrar configuración actual
    current_config = service.get_quick_pass_config()
    
    click.echo("# Quick Pass - Sistema de fichaje")
    click.echo(f"QUICK_PASS_URL={current_config.get('url', 'https://tu-sistema-fichaje.com')}")
    click.echo(f"QUICK_PASS_INGRESS={current_config.get('ingress', 'tu-codigo-ingreso')}")
    click.echo(f"QUICK_PASS_LEGAJO={current_config.get('legajo', 'tu-legajo')}")
    click.echo(f"QUICK_PASS_PIN={current_config.get('pin', 'tu-pin')}")
    click.echo()
    click.echo("# Configuración de logs (opcional)")
    click.echo("# Si no se especifica, se usa ~/.config/client-infs/logs/")
    click.echo("# LOGS_PATH=/ruta/personalizada/para/logs")
    
    show_separator()
    
    # Mostrar información actual de logs
    from client_infs.config.settings import settings
    click.echo(f"📁 Directorio actual de logs: {settings.logs_dir}")
    
    if os.getenv("LOGS_PATH"):
        click.echo("✅ Usando directorio personalizado desde LOGS_PATH")
    else:
        click.echo("📌 Usando directorio por defecto (configurar LOGS_PATH para personalizar)")
    
    show_separator()
    click.echo("📝 Instrucciones:")
    click.echo("1. Abre el archivo .env en tu editor preferido")
    click.echo("2. Agrega o actualiza las variables QUICK_PASS_*")
    click.echo("3. Opcionalmente, configura LOGS_PATH para logs personalizados")
    click.echo("4. Guarda el archivo y reinicia la aplicación")
    show_separator()
    click.echo("⚠️  Importante: Nunca compartas tu archivo .env con credenciales")
    
    if click.confirm("\n¿Abrir el archivo .env para editar?"):
        try:
            import subprocess
            import sys
            
            if sys.platform == "win32":
                subprocess.run(["notepad", str(config_file)])
            elif sys.platform == "darwin":
                subprocess.run(["open", str(config_file)])
            else:
                subprocess.run(["nano", str(config_file)])
                
        except Exception as e:
            click.echo(f"❌ Error abriendo editor: {e}")
            click.echo(f"Abre manualmente: {config_file}")