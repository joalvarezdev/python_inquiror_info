"""
Servicio para la gestión de clientes.
"""

import base64
import json
from typing import Dict

import requests

from client_infs.config.settings import settings


class ClientService:
    """Servicio para crear y gestionar clientes."""
    
    def __init__(self, environment: str = "testing"):
        self.environment = environment
        self.base_url = settings.get_base_url(environment)
        self.username = settings.auth_username
        self.password = settings.auth_password

    def get_access_token(self) -> str:
        """Obtiene el token de acceso usando las credenciales del archivo .env."""
        credentials = f"{self.username}:{self.password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        url = f"{self.base_url}/oauth/token?grant_type=client_credentials"
        headers = {
            "Authorization": f"Basic {encoded_credentials}"
        }
        
        try:
            response = requests.post(url, headers=headers)
            response.raise_for_status()
            return response.json()["access_token"]
        except requests.RequestException as e:
            raise Exception(f"Error obteniendo token de acceso: {e}")
        except KeyError:
            raise Exception("Respuesta inesperada del servidor al obtener token")

    def create_client(self, client_data: Dict, access_token: str) -> Dict:
        """Crea un nuevo cliente usando el token de acceso."""
        url = f"{self.base_url}/signup-client"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        
        try:
            response = requests.post(url, headers=headers, json=client_data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Error creando cliente: {e}")

    def get_default_client_data(self, client_id: str) -> Dict:
        """Retorna la configuración estándar para testing con solo el clientId variable."""
        return {
            "accessTokenValidity": 30000,
            "authorities": "ANONYMOUS,USER,ADMIN", 
            "authorizedGrantTypes": "authorization_code,client_credentials,password,refresh_token",
            "autoapprove": "true",
            "clientId": client_id,
            "clientSecret": "infosis",
            "refreshTokenValidity": 36000,
            "scope": "ANONYMOUS_READ,ANONYMOUS_WRITE,USER_READ,USER_WRITE,ADMIN_READ,ADMIN_WRITE"
        }