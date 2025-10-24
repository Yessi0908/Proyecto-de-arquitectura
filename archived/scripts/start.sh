#!/bin/bash

# Script de inicio del Sistema de Invernadero IoT
# Resuelve problemas comunes de configuración

echo "🌿 Iniciando Sistema de Invernadero Automatizado..."

# Verificar si Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado"
    echo "💡 Instalar Docker Desktop desde: https://www.docker.com/products/docker-desktop"
    exit 1
fi

# Verificar si Docker está ejecutándose
if ! docker info &> /dev/null; then
    echo "⚠️  Docker no está ejecutándose"
    echo "🔄 Intentando iniciar Docker..."
    
    # Para Windows
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        powershell.exe -Command "Start-Process 'C:\Program Files\Docker\Docker\Docker Desktop.exe'"
        echo "⏳ Esperando a que Docker se inicie..."
        sleep 30
    # Para macOS
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        open -a Docker
        echo "⏳ Esperando a que Docker se inicie..."
        sleep 30
    # Para Linux
    else
        sudo systemctl start docker
        sleep 10
    fi
    
    # Verificar de nuevo
    if ! docker info &> /dev/null; then
        echo "❌ No se pudo iniciar Docker automáticamente"
        echo "💡 Iniciarlo manualmente y ejecutar este script de nuevo"
        exit 1
    fi
fi

echo "✅ Docker está funcionando"

# Crear red personalizada si no existe
docker network create invernadero-net 2>/dev/null || echo "ℹ️  Red ya existe"

# Detener contenedores previos
echo "🔄 Limpiando contenedores anteriores..."
docker-compose down 2>/dev/null

# Construir e iniciar servicios
echo "🚀 Iniciando servicios del invernadero..."
docker-compose up --build -d

# Esperar a que los servicios se inicien
echo "⏳ Esperando a que los servicios se inicien..."
sleep 15

# Verificar estado de los servicios
echo "📊 Estado de los servicios:"
docker-compose ps

# Inicializar base de datos
echo "🗄️  Inicializando base de datos..."
sleep 5
curl -X POST http://localhost:5000/api/init -H "Content-Type: application/json" -d "{}" 2>/dev/null

# Verificar conectividad
echo "🔍 Verificando conectividad..."
if curl -s http://localhost:5000 > /dev/null; then
    echo "✅ Sistema iniciado correctamente!"
    echo ""
    echo "🌐 Acceder al dashboard: http://localhost:5000"
    echo "📊 Ver estadísticas: http://localhost:5000/static/estadisticas.html"
    echo "📄 Documentación: /docs/"
    echo ""
    echo "🤖 Para configurar Arduino, revisar: /arduino/README_ARDUINO.md"
else
    echo "❌ Error: No se puede acceder al sistema"
    echo "🔧 Verificar logs con: docker-compose logs"
fi