# Script de inicio para Windows PowerShell
# Sistema de Invernadero Automatizado IoT

Write-Host "🌿 Iniciando Sistema de Invernadero Automatizado..." -ForegroundColor Green

# Verificar si Docker está instalado
try {
    docker --version | Out-Null
    Write-Host "✅ Docker está instalado" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker no está instalado" -ForegroundColor Red
    Write-Host "💡 Instalar Docker Desktop desde: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

# Verificar si Docker está ejecutándose
try {
    docker info | Out-Null
    Write-Host "✅ Docker está funcionando" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Docker no está ejecutándose" -ForegroundColor Yellow
    Write-Host "🔄 Intentando iniciar Docker Desktop..." -ForegroundColor Cyan
    
    try {
        Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
        Write-Host "⏳ Esperando a que Docker se inicie..." -ForegroundColor Cyan
        Start-Sleep -Seconds 45
        
        # Verificar de nuevo
        docker info | Out-Null
        Write-Host "✅ Docker iniciado correctamente" -ForegroundColor Green
    } catch {
        Write-Host "❌ No se pudo iniciar Docker automáticamente" -ForegroundColor Red
        Write-Host "💡 Iniciar Docker Desktop manualmente y ejecutar este script de nuevo" -ForegroundColor Yellow
        Read-Host "Presionar Enter para continuar..."
        exit 1
    }
}

# Navegar al directorio del proyecto
$projectPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectPath

# Detener contenedores previos
Write-Host "🔄 Limpiando contenedores anteriores..." -ForegroundColor Cyan
docker-compose down 2>$null

# Construir e iniciar servicios
Write-Host "🚀 Iniciando servicios del invernadero..." -ForegroundColor Green
docker-compose up --build -d

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error iniciando servicios" -ForegroundColor Red
    Write-Host "🔧 Verificar docker-compose.yml y logs" -ForegroundColor Yellow
    Read-Host "Presionar Enter para continuar..."
    exit 1
}

# Esperar a que los servicios se inicien
Write-Host "⏳ Esperando a que los servicios se inicien..." -ForegroundColor Cyan
Start-Sleep -Seconds 20

# Verificar estado de los servicios
Write-Host "📊 Estado de los servicios:" -ForegroundColor Cyan
docker-compose ps

# Inicializar base de datos
Write-Host "🗄️  Inicializando base de datos..." -ForegroundColor Cyan
Start-Sleep -Seconds 5

try {
    Invoke-RestMethod -Uri "http://localhost:5000/api/init" -Method POST -ContentType "application/json" -Body "{}" | Out-Null
    Write-Host "✅ Base de datos inicializada" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Error inicializando BD (puede ser normal si ya existe)" -ForegroundColor Yellow
}

# Verificar conectividad
Write-Host "🔍 Verificando conectividad..." -ForegroundColor Cyan
try {
    Invoke-WebRequest -Uri "http://localhost:5000" -UseBasicParsing | Out-Null
    Write-Host "" 
    Write-Host "✅ ¡Sistema iniciado correctamente!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🌐 Acceder al dashboard: " -NoNewline -ForegroundColor Cyan
    Write-Host "http://localhost:5000" -ForegroundColor White
    Write-Host "📊 Ver estadísticas: " -NoNewline -ForegroundColor Cyan  
    Write-Host "http://localhost:5000/static/estadisticas.html" -ForegroundColor White
    Write-Host "📄 Documentación: " -NoNewline -ForegroundColor Cyan
    Write-Host "/docs/" -ForegroundColor White
    Write-Host ""
    Write-Host "🤖 Para configurar Arduino, revisar: /arduino/README_ARDUINO.md" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Presionar Enter para abrir el dashboard..." -ForegroundColor Green
    Read-Host
    Start-Process "http://localhost:5000"
} catch {
    Write-Host "❌ Error: No se puede acceder al sistema" -ForegroundColor Red
    Write-Host "🔧 Verificar logs con: docker-compose logs" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Comandos útiles:" -ForegroundColor Cyan
    Write-Host "  docker-compose logs backend" -ForegroundColor White
    Write-Host "  docker-compose logs db" -ForegroundColor White
    Write-Host "  docker-compose restart" -ForegroundColor White
    Read-Host "Presionar Enter para salir..."
}