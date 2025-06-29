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

### Instalacion Rapida

```bash
# Clonar el repositorio
git clone https://github.com/joalvarezdev/python_inquiror_info.git
cd client-infs

# Ejecutar script de instalacion automatica
./install.sh
```

### Instalacion Manual

#### 1. Clonar el repositorio

```bash
git clone https://github.com/joalvarezdev/python_inquiror_info.git
cd client-infs
```

#### 2. Opciones de instalacion

##### Opcion A: Con UV (recomendado)

```bash
# Instalar uv si no lo tienes
curl -LsSf https://astral.sh/uv/install.sh | sh

# Crear entorno virtual e instalar dependencias
uv venv
source .venv/bin/activate
uv pip install -e .
```

##### Opcion B: Con venv tradicional

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

##### Opcion C: Instalacion directa desde GitHub

```bash
# Con pip
pip install git+https://github.com/joalvarezdev/python_inquiror_info.git@v0.1.0

# Con uv
uv add git+https://github.com/joalvarezdev/python_inquiror_info.git@v0.1.0
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

### Comandos Disponibles

Despues de la instalacion, puedes usar estos comandos:

```bash
# Activar entorno virtual (si usaste instalacion manual)
source .venv/bin/activate

# Comandos principales
inf       # Menu principal de la aplicacion
quick     # Quick pass flow - fichar rapidamente
connect   # Conectar a servidor
restart   # Reiniciar servidor
srvinf    # Mostrar informacion del servidor
```

### Ejecutar desde codigo fuente

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

## Releases

### Descarga la version estable

Puedes descargar la version mas reciente desde [GitHub Releases](https://github.com/joalvarezdev/python_inquiror_info/releases).

### Historial de versiones

- **v0.1.0** - Primera version estable
  - Gestion de clientes y servidores
  - Quick pass flow
  - Comandos CLI completos

## API y Configuracion

### Variables de entorno disponibles

| Variable | Descripcion | Valor por defecto |
|----------|-------------|-------------------|
| `AUTH_USERNAME` | Usuario para autenticacion | `zeus` |
| `AUTH_PASSWORD` | Contraseña para autenticacion | `infosis` |
| `BASE_URL` | URL del entorno de testing | `https://auth-test.infosis.tech` |
| `PROD_BASE_URL` | URL del entorno de produccion | `https://auth.infosis.tech` |

### Estructura de comandos

```bash
client_infs/
├── cli.py                    # Punto de entrada principal
├── ui/
│   ├── menus.py             # Menus interactivos
│   ├── client_flows.py      # Flujos de gestion de clientes
│   ├── quick_pass_flows.py  # Flujo de fichaje rapido
│   └── servers_flows.py     # Gestion de servidores
└── services/
    ├── client_service.py    # Servicios de cliente
    ├── quick_pass_service.py # Servicios de fichaje
    └── server_service.py    # Servicios de servidor
```

## Desarrollo

### Configuracion del entorno de desarrollo

```bash
# Clonar el repositorio
git clone https://github.com/joalvarezdev/python_inquiror_info.git
cd client-infs

# Instalar dependencias de desarrollo
uv sync --dev

# Ejecutar tests (si existen)
pytest

# Linting
ruff check .
```

## Proximas Funcionalidades

- [ ] Soporte completo para entorno de produccion
- [ ] Listado y gestion de clientes existentes
- [ ] Configuracion personalizada de clientes
- [ ] Exportacion de configuraciones
- [ ] Logs y auditoria
- [ ] Tests automatizados
- [ ] Documentacion de API

## Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

### Codigo de conducta

- Sigue las convenciones de codigo existentes
- Incluye tests para nuevas funcionalidades
- Actualiza la documentacion cuando sea necesario
- Usa commits descriptivos

## Licencia

Este proyecto esta bajo la Licencia MIT. Ver archivo `LICENSE` para mas detalles.

## Soporte

Si tienes problemas o preguntas:

1. Revisa la seccion de [Solucion de Problemas](#solucion-de-problemas)
2. Consulta los [Issues existentes](https://github.com/joalvarezdev/python_inquiror_info/issues)
3. Abre un [nuevo Issue](https://github.com/joalvarezdev/python_inquiror_info/issues/new)
4. Contacta al equipo de desarrollo

---

**Equipo INFOSIS** - Aplicacion de consola para gestion de clientes y servidores