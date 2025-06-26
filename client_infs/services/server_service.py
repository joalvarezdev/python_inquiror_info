import re
import configparser
import sys
import subprocess
import os

from client_infs.config.settings import settings

class ServerService:
    """Servicio para interactuar con servidores"""
    def __init__(self):
        self.config_path = settings.server_file

    def __get_all_servers(self) -> dict:
        """Lee la información de los servidores desde un archivo."""

        with open(self.config_path, 'r') as file:
            config_content = '[DEFAULT]\n' + file.read()

        config = configparser.ConfigParser()
        config.read_string(config_content)

        servers = {}
        for section in config.sections():
            servers[section] = {
                'ip': config[section].get('ip', '').strip(),
                'user': config[section].get('user', '').strip(),
                'password': config[section].get('password', '').strip()
            }

        return servers


    def __get_server_info(self, server_name: str) -> dict:
        servers = self.__get_all_servers()
        return servers[server_name]


    def get_name_servers(self) -> list:
        """Obtiene una lista de todos los servidores."""
        response = []

        servers = self.__get_all_servers()

        for server in servers.keys():
            response.append({"name": server, "value": server})

        response.append({"name": "← Volver al menú de gestión", "value": "back"})

        return response 



    def show_server_info(self, server_name: str):
        """Muestra la información del servidor especificado."""
        server_info = self.__get_server_info(server_name)
        print(f"IP: {server_info['ip']}")
        print(f"username: {server_info['user']}")
        print(f"password: {server_info['password']}")


    def restart_server(self, server_name: str):
        """Reinicia el servidor especificado."""
        server = self.__get_server_info(server_name)
        try:
            command = (f"echo '{server['password']}' | sshpass -p {server['password']} "
                      f"ssh {server['user']}@{server['ip']} 'sudo -S reboot now'")
            os.system(command)

        except subprocess.CalledProcessError as e:
            print(f"Error al conectar con el servidor: {e}")
            sys.exit(1)


    def connect_to_server(self, server_name: str):
        """Conecta al servidor especificado."""
        server = self.__get_server_info(server_name)
        try:
            subprocess.run(
                ["sshpass", "-p", server['password'],
                 "ssh", f"{server['user']}@{server['ip']}"],
                check=True
            )
        except subprocess.CalledProcessError as e:
            print(f"Error al conectar con el servidor: {e}")
            sys.exit(1)
