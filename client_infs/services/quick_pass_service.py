"""
Servicio para Quick Pass - Sistema de fichaje automático.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

import click
import pyperclip
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

from client_infs.config.settings import settings


class QuickPassService:
    """Servicio para automatizar el fichaje de entrada/salida."""
    
    def __init__(self):
        self.config_dir = settings.config_dir
        self.logs_dir = settings.logs_dir
        
    def get_quick_pass_config(self) -> dict:
        """Obtiene la configuración de Quick Pass desde variables de entorno."""
        return {
            "url": os.getenv("QUICK_PASS_URL", ""),
            "ingress": os.getenv("QUICK_PASS_INGRESS", ""),
            "legajo": os.getenv("QUICK_PASS_LEGAJO", ""),
            "pin": os.getenv("QUICK_PASS_PIN", "")
        }
    
    def validate_config(self, config: dict) -> bool:
        """Valida que la configuración tenga todos los campos requeridos."""
        required_fields = ["url", "ingress", "legajo", "pin"]
        return all(config.get(field) for field in required_fields)
    
    def setup_chrome_driver(self, headless: bool = True) -> tuple:
        """Configura e inicializa el Chrome WebDriver."""
        chrome_options = Options()
        
        # Modo headless configurable
        if headless:
            chrome_options.add_argument("--headless")  # Ejecutar sin GUI
            
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        
        try:
            # Intentar crear el driver
            driver = webdriver.Chrome(options=chrome_options)
            wait = WebDriverWait(driver, 10)
            return driver, wait
        except Exception as e:
            error_msg = f"❌ Error inicializando Chrome WebDriver: {str(e)}"
            
            # Mensajes de error más específicos
            if "chromedriver" in str(e).lower():
                error_msg += "\\n\\n💡 Soluciones posibles:"
                error_msg += "\\n   1. Instalar ChromeDriver: sudo apt install chromium-chromedriver"
                error_msg += "\\n   2. O descargar desde: https://chromedriver.chromium.org/"
                error_msg += "\\n   3. Asegúrate de que esté en tu PATH"
            elif "chrome" in str(e).lower():
                error_msg += "\\n\\n💡 Soluciones posibles:"
                error_msg += "\\n   1. Instalar Google Chrome o Chromium"
                error_msg += "\\n   2. sudo apt install google-chrome-stable"
                error_msg += "\\n   3. O: sudo apt install chromium-browser"
                
            raise Exception(error_msg)
    
    def click_button(self, wait, button_id: str):
        """Hace clic en un botón identificado por ID."""
        try:
            button = wait.until(EC.element_to_be_clickable((By.ID, button_id)))
            button.click()
        except Exception as e:
            raise Exception(f"Error haciendo clic en botón {button_id}: {e}")
    
    def send_keys_to_field(self, driver, wait, field_id: str, text: str):
        """Envía texto a un campo identificado por ID."""
        try:
            # Esperar a que el elemento esté presente Y visible
            field = wait.until(EC.visibility_of_element_located((By.ID, field_id)))
            
            # Asegurar que es interactuable
            wait.until(EC.element_to_be_clickable((By.ID, field_id)))
            
            # Hacer scroll al elemento si es necesario
            self._scroll_to_element(driver, field)
            
            # Limpiar y escribir
            field.clear()
            field.send_keys(text)
            
            # Verificar que el texto se escribió
            import time
            time.sleep(0.5)  # Pequeña pausa para que se procese
            
        except Exception as e:
            raise Exception(f"Error enviando texto al campo {field_id}: {e}")
    
    def _scroll_to_element(self, driver, element):
        """Hace scroll a un elemento para asegurar que sea visible."""
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            import time
            time.sleep(0.3)  # Pausa para que termine el scroll
        except Exception:
            pass  # Si falla el scroll, continuar
    
    def get_div_text(self, driver, div_id: str) -> str:
        """Obtiene el texto de un div identificado por ID."""
        try:
            div = driver.find_element(By.ID, div_id)
            return div.text.strip()
        except Exception as e:
            return f"Error obteniendo texto del div {div_id}: {e}"
    
    def save_registry(self, status: str):
        """Guarda el registro del fichaje en logs organizados por fecha."""
        # Solo guardar si el status indica éxito
        if not ("Ingreso" in status and "correcto" in status):
            return
            
        now = datetime.now()
        year = now.strftime("%Y")
        month = now.strftime("%b")
        
        # Crear estructura de directorios
        year_dir = self.logs_dir / year
        year_dir.mkdir(parents=True, exist_ok=True)
        
        # Archivo de logs del mes
        log_file = year_dir / f"{month}.json"
        
        # Cargar logs existentes o crear nuevo
        logs = []
        if log_file.exists():
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                logs = []
        
        # Agregar nuevo registro
        new_entry = {
            "timestamp": now.isoformat(),
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S"),
            "day": now.strftime("%A"),
            "status": status
        }
        
        logs.append(new_entry)
        
        # Guardar logs actualizados
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
    
    def perform_quick_pass(self, headless: bool = True) -> str:
        """Ejecuta el proceso completo de Quick Pass."""
        # Obtener configuración
        config = self.get_quick_pass_config()
        
        if not self.validate_config(config):
            return "❌ Configuración incompleta. Verifica las variables de entorno QUICK_PASS_*"
        
        driver = None
        try:
            # Configurar WebDriver
            driver, wait = self.setup_chrome_driver(headless)
            
            # Navegar a la página
            driver.get(config["url"])
            
            # Dar tiempo a que cargue la página
            import time
            time.sleep(2)
            
            # Proceso de fichaje con pausas adicionales
            self.click_button(wait, "btnComenzar")
            time.sleep(1)
            
            self.send_keys_to_field(driver, wait, "sensor_manual", config["ingress"])
            time.sleep(1)
            
            self.click_button(wait, "btnReiniciar")
            time.sleep(3)  # Pausa más larga después de reiniciar
            
            # Intentar el campo legajo con retry
            self._send_keys_with_retry(driver, wait, "legajo", config["legajo"])
            time.sleep(1)
            
            self._send_keys_with_retry(driver, wait, "pin", config["pin"])
            time.sleep(1)
            
            self.click_button(wait, "btnFichar")
            time.sleep(2)  # Esperar a que procese
            
            # Obtener resultado
            status = self.get_div_text(driver, "divLog")
            
            # Guardar registro
            self.save_registry(status)
            
            # Copiar al portapapeles
            pyperclip.copy(status)
            
            return status
            
        except Exception as e:
            error_msg = f"❌ Error en Quick Pass: {e}"
            return error_msg
        finally:
            if driver:
                driver.quit()
    
    def get_recent_logs(self, days: int = 7) -> list:
        """Obtiene los logs recientes de fichaje."""
        logs = []
        now = datetime.now()
        
        # Buscar en el mes actual
        year = now.strftime("%Y")
        month = now.strftime("%b")
        log_file = self.logs_dir / year / f"{month}.json"
        
        if log_file.exists():
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    all_logs = json.load(f)
                
                # Filtrar logs recientes
                cutoff = now.timestamp() - (days * 24 * 60 * 60)
                for log in all_logs:
                    log_time = datetime.fromisoformat(log["timestamp"]).timestamp()
                    if log_time >= cutoff:
                        logs.append(log)
                        
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        
        return sorted(logs, key=lambda x: x["timestamp"], reverse=True)
    
    def _send_keys_with_retry(self, driver, wait, field_id: str, text: str, max_retries: int = 3):
        """Envía texto a un campo con reintentos."""
        for attempt in range(max_retries):
            try:
                # Primero intentar hacer clic en el campo para activarlo
                field = wait.until(EC.element_to_be_clickable((By.ID, field_id)))
                field.click()
                
                import time
                time.sleep(0.5)
                
                # Luego enviar el texto
                self.send_keys_to_field(driver, wait, field_id, text)
                return  # Éxito
                
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e  # Último intento, lanzar excepción
                
                # Pausa antes del siguiente intento
                import time
                time.sleep(2)
                
                # Si es el primer retry, intentar refrescar la página
                if attempt == 0:
                    try:
                        driver.refresh()
                        time.sleep(3)
                        # Repetir pasos anteriores
                        self.click_button(wait, "btnComenzar")
                        time.sleep(1)
                        self.send_keys_to_field(driver, wait, "sensor_manual", self.get_quick_pass_config()["ingress"])
                        time.sleep(1)
                        self.click_button(wait, "btnReiniciar")
                        time.sleep(3)
                    except:
                        pass