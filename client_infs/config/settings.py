"""
Configuración y settings de la aplicación.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv


def get_config_dir():
    """Obtiene el directorio de configuración según el entorno."""
    # Si existe .env local, usar directorio actual
    if Path(".env").exists():
        return Path(".")
    
    # Si no, usar directorio global
    if sys.platform == "win32":
        return Path.home() / "AppData" / "Local" / "client-infs"
    else:
        return Path.home() / ".config" / "client-infs"


# Cargar configuración desde directorio apropiado
config_dir = get_config_dir()
env_file = config_dir / ".env"

if env_file.exists():
    load_dotenv(env_file)
else:
    load_dotenv()  # Fallback a variables de entorno del sistema


class Settings:
    """Configuración de la aplicación."""
    
    def __init__(self):
        self.auth_username = os.getenv("AUTH_USERNAME", "zeus")
        self.auth_password = os.getenv("AUTH_PASSWORD", "infosis")
        self.base_url_testing = os.getenv("BASE_URL", "https://auth-test.infosis.tech")
        self.base_url_production = os.getenv("PROD_BASE_URL", "https://auth.infosis.tech")
        self.server_file = os.getenv("SERVER_INFO_FILE_PATH", "")
        self.config_dir = config_dir
        
        # Configuración de logs - usar variable de entorno o directorio por defecto
        logs_path = os.getenv("LOGS_PATH")
        if logs_path:
            self.logs_dir = Path(logs_path)
        else:
            # Directorio por defecto en la configuración del usuario
            self.logs_dir = config_dir / "logs"
    
    def get_base_url(self, environment: str) -> str:
        """Obtiene la URL base según el entorno."""
        if environment.lower() == "testing":
            return self.base_url_testing
        elif environment.lower() == "production":
            return self.base_url_production
        else:
            raise ValueError(f"Entorno no válido: {environment}")


settings = Settings()