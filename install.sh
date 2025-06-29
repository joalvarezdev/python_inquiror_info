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