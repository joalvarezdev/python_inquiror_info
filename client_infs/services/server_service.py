
class ServerService:
    """Servicio para interactuar con servidores"""

    def _get_server_info(sefl) -> dict:
       print("Hola mundo") 

    def get_server_info(self, server_name: str):
        """Obtiene información del servidor especificado."""
        # Aquí se implementaría la lógica para obtener la información del servidor
        # Por ejemplo, leer de un archivo o base de datos
        return {
            "name": server_name,
            "url": "http://example.com",
            "credentials": {
                "username": "admin",
                "password": "password123"
            }
        }