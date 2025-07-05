#!/bin/bash

set -e

echo "🚀 Instalando Cliente INFOSIS..."

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado. Por favor instálalo primero."
    exit 1
fi

# Verificar versión de Python
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:3])))')
REQUIRED_VERSION="3.10.12"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Se requiere Python $REQUIRED_VERSION o superior. Versión actual: $PYTHON_VERSION"
    echo ""
    echo "💡 Opciones para instalar Python $REQUIRED_VERSION:"
    
    # Detectar sistema operativo y gestor de paquetes
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command -v apt &> /dev/null; then
            echo "  🐧 Ubuntu/Debian: sudo apt update && sudo apt install python3.10 python3.10-venv"
        elif command -v yum &> /dev/null; then
            echo "  🔴 CentOS/RHEL: sudo yum install python3.10"
        elif command -v dnf &> /dev/null; then
            echo "  🔴 Fedora: sudo dnf install python3.10"
        elif command -v pacman &> /dev/null; then
            echo "  🏃 Arch: sudo pacman -S python"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        if command -v brew &> /dev/null; then
            echo "  🍎 macOS (Homebrew): brew install python@3.10"
        else
            echo "  🍎 macOS: Instala Homebrew primero: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
            echo "           Luego: brew install python@3.10"
        fi
    fi
    
    echo ""
    echo "🔧 Alternativa con pyenv (recomendado):"
    echo "  1. Instalar pyenv: curl https://pyenv.run | bash"
    echo "  2. Reiniciar terminal o ejecutar: source ~/.bashrc"
    echo "  3. Instalar Python: pyenv install 3.10.12"
    echo "  4. Usar como global: pyenv global 3.10.12"
    echo ""
    echo "📖 Más información: https://github.com/pyenv/pyenv#installation"
    
    exit 1
fi

# Verificar si pip está disponible
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 no está instalado. Instálalo con:"
    echo "  🐧 Ubuntu/Debian: sudo apt install python3-pip"
    echo "  🔴 CentOS/RHEL: sudo yum install python3-pip"
    echo "  🔴 Fedora: sudo dnf install python3-pip"
    echo "  🍎 macOS: python3 -m ensurepip --upgrade"
    exit 1
fi

# Crear entorno virtual e instalar dependencias
echo "🔧 Configurando entorno virtual..."
python3 -m venv .venv
source .venv/bin/activate

# Actualizar pip
echo "📦 Actualizando pip..."
pip3 install --upgrade pip

echo "📦 Instalando dependencias..."
pip3 install -r requirements.txt
pip3 install -e .

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