# Gestion de Clientes

Aplicacion de consola para crear y gestionar clientes en el sistema de autenticacion INFOSIS.

## Caracteristicas

- Interfaz de consola intuitiva con navegacion vim (hjkl)
- Soporte para entornos Testing y Produccion
- Configuracion centralizada con archivos .env
- Arquitectura modular y escalable
- Gestion automatica de tokens de autenticacion

## Estructura del Proyecto

```
client-infs/
├── src/
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py          # Configuracion centralizada
│   ├── services/
│   │   ├── __init__.py
│   │   └── client_service.py    # Logica de negocio
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── menus.py            # Menus de interfaz
│   │   └── client_flows.py     # Flujos de usuario
│   └── __init__.py
├── main.py                     # Punto de entrada
├── .env.example               # Plantilla de configuracion
├── .vscode/                   # Configuracion VS Code
├── pyproject.toml            # Dependencias del proyecto
└── README.md                 # Este archivo
```

## Instalacion y Configuracion

### Prerrequisitos

- Python 3.11 o superior
- Git

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd client-infs
```

### 2. Opciones de instalacion

#### Opcion A: Instalacion Global (recomendado para uso diario)

```bash
# Instalar globalmente
pip install .

# Configurar archivos de configuracion
python setup_global.py

# Usar desde cualquier lugar
client-infs
# o
infosis-client
```

#### Opcion B: Con UV (recomendado para desarrollo)

```bash
# Instalar uv si no lo tienes
pip install uv

# Instalar dependencias
uv sync

# Ejecutar aplicacion
uv run main.py
```

#### Opcion C: Con venv tradicional (recomendado para VS Code)

```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# En Linux/Mac:
source .venv/bin/activate
# En Windows:
.venv\Scripts\activate

# Instalar dependencias
pip install -e .
```

### 3. Configurar variables de entorno

#### Para instalacion global:
El archivo de configuracion se crea automaticamente en:
- **Linux/Mac:** `~/.config/client-infs/.env`
- **Windows:** `%LOCALAPPDATA%/client-infs/.env`

#### Para desarrollo local:
```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus credenciales
nano .env
```

Contenido del archivo `.env`:

```env
# Configuracion de autenticacion
AUTH_USERNAME=zeus
AUTH_PASSWORD=infosis

# URLs de los entornos
BASE_URL=https://auth-test.infosis.tech
PROD_BASE_URL=https://auth.infosis.tech
```

## Configuracion de VS Code

### Automatica
La configuracion esta incluida en `.vscode/settings.json` y deberia funcionar automaticamente.

### Manual (si es necesario)

1. **Seleccionar interprete de Python:**
   - `Ctrl/Cmd + Shift + P`
   - Buscar: "Python: Select Interpreter"
   - Seleccionar: `./.venv/bin/python`

2. **Si persisten los warnings de imports:**
   - Instalar extension "Python" de Microsoft
   - Reiniciar VS Code despues de activar el entorno virtual

## Uso de la Aplicacion

### Ejecutar la aplicacion

```bash
# Con entorno virtual activado
python main.py

# O con uv
uv run main.py
```

### Controles de navegacion

- **j/k** - Bajar/Subir (vim style)
- **↑/↓** - Flechas tradicionales
- **Enter** - Seleccionar opcion
- **Ctrl+C** - Salir

### Flujo de uso

1. **Menu principal:**
   ```
   ? Seleccione una opcion:
   > Crear cliente
     Salir
   ```

2. **Seleccion de entorno:**
   ```
   ? Seleccione el entorno:
   > Testing
     Produccion (proximamente)
     ← Volver al menu principal
   ```

3. **Creacion de cliente:**
   - Ingresa el ID del cliente
   - Confirma la configuracion estandar
   - El sistema crea el cliente automaticamente

## Configuracion de Cliente

La aplicacion usa configuracion estandar para testing:

```json
{
  "accessTokenValidity": 30000,
  "authorities": "ANONYMOUS,USER,ADMIN",
  "authorizedGrantTypes": "authorization_code,client_credentials,password,refresh_token",
  "autoapprove": "true",
  "clientId": "[ID_INGRESADO]",
  "clientSecret": "infosis",
  "refreshTokenValidity": 36000,
  "scope": "ANONYMOUS_READ,ANONYMOUS_WRITE,USER_READ,USER_WRITE,ADMIN_READ,ADMIN_WRITE"
}
```

## Solucion de Problemas

### Error: "Input is not a terminal"
- Ejecuta la aplicacion desde una terminal real, no desde un IDE integrado

### Warnings de imports en VS Code
- Asegurate de tener el entorno virtual activado
- Selecciona el interprete correcto en VS Code
- Reinicia VS Code despues de la configuracion

### Error de autenticacion
- Verifica que el archivo `.env` tenga las credenciales correctas
- Confirma que el endpoint este accesible

### Problemas con dependencias
```bash
# Limpiar e instalar de nuevo
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Proximas Funcionalidades

- [ ] Soporte completo para entorno de produccion
- [ ] Listado y gestion de clientes existentes
- [ ] Configuracion personalizada de clientes
- [ ] Exportacion de configuraciones
- [ ] Logs y auditoria

## Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## Licencia

Este proyecto esta bajo la Licencia MIT.

## Soporte

Si tienes problemas o preguntas:

1. Revisa la seccion de Solucion de Problemas
2. Abre un Issue en GitHub
3. Contacta al equipo de desarrollo