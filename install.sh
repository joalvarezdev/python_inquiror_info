#!/bin/bash

set -e

echo "🚀 Instalando Cliente INFOSIS..."

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado. Por favor instálalo primero."
    exit 1
fi

# Verificar versión de Python
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.11"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Se requiere Python $REQUIRED_VERSION o superior. Versión actual: $PYTHON_VERSION"
    echo ""
    echo "💡 Opciones para instalar Python $REQUIRED_VERSION:"
    
    # Detectar sistema operativo y gestor de paquetes
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command -v apt &> /dev/null; then
            echo "  🐧 Ubuntu/Debian: sudo apt update && sudo apt install python3.11 python3.11-venv"
        elif command -v yum &> /dev/null; then
            echo "  🔴 CentOS/RHEL: sudo yum install python3.11"
        elif command -v dnf &> /dev/null; then
            echo "  🔴 Fedora: sudo dnf install python3.11"
        elif command -v pacman &> /dev/null; then
            echo "  🏃 Arch: sudo pacman -S python"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        if command -v brew &> /dev/null; then
            echo "  🍎 macOS (Homebrew): brew install python@3.11"
        else
            echo "  🍎 macOS: Instala Homebrew primero: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
            echo "           Luego: brew install python@3.11"
        fi
    fi
    
    echo ""
    echo "🔧 Alternativa con pyenv (recomendado):"
    echo "  1. Instalar pyenv: curl https://pyenv.run | bash"
    echo "  2. Reiniciar terminal o ejecutar: source ~/.bashrc"
    echo "  3. Instalar Python: pyenv install 3.11.9"
    echo "  4. Usar como global: pyenv global 3.11.9"
    echo ""
    echo "📖 Más información: https://github.com/pyenv/pyenv#installation"
    
    exit 1
fi

# Instalar uv si no está disponible
if ! command -v uv &> /dev/null; then
    echo "📦 Instalando uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.cargo/env
fi

# Crear entorno virtual e instalar dependencias
echo "🔧 Configurando entorno virtual..."
uv venv
source .venv/bin/activate

echo "📦 Instalando dependencias..."
uv pip install -e .

echo "✅ Instalación completada!"
echo ""
echo "📋 Comandos disponibles:"
echo "  • inf       - Menú principal"
echo "  • quick     - Quick pass flow"
echo "  • connect   - Conectar a servidor"
echo "  • restart   - Reiniciar servidor"
echo "  • srvinf    - Información del servidor"
echo ""
echo "🎯 Para usar los comandos, activa el entorno virtual:"
echo "   source .venv/bin/activate"