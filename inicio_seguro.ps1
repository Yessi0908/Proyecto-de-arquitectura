#!/usr/bin/env powershell
# Script de inicio para el servidor seguro del invernadero

Write-Host "🌿 SISTEMA DE INVERNADERO - INICIO SEGURO" -ForegroundColor Green
Write-Host "=" -ForegroundColor Green -NoNewline; 1..50 | ForEach-Object { Write-Host "=" -ForegroundColor Green -NoNewline }; Write-Host ""

# Cambiar al directorio del proyecto
$projectDir = "C:\Users\ingri\OneDrive\Documents\Custom Office Templates\Desktop\Arquitectura\ProyectoInvernadero\Proyecto-de-arquitectura"
Set-Location $projectDir

Write-Host "📁 Directorio de trabajo: $projectDir" -ForegroundColor Cyan

# Activar entorno virtual
Write-Host "🔧 Activando entorno virtual..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1

# Verificar certificados SSL
if ((Test-Path "server.crt") -and (Test-Path "server.key")) {
    Write-Host "🔒 Certificados SSL encontrados - HTTPS habilitado" -ForegroundColor Green
} else {
    Write-Host "⚠️  Certificados SSL no encontrados - Generando..." -ForegroundColor Yellow
    python generar_certificado.py
    Write-Host "✅ Certificados generados" -ForegroundColor Green
}

# Verificar dependencias
Write-Host "📦 Verificando dependencias..." -ForegroundColor Yellow
pip install -q reportlab pymysql flask flask-cors pyopenssl

Write-Host ""
Write-Host "🚀 INICIANDO SERVIDOR SEGURO..." -ForegroundColor Green
Write-Host "🔒 URL segura: https://localhost:5000" -ForegroundColor Cyan
Write-Host "🔒 URL red local: https://192.168.1.7:5000" -ForegroundColor Cyan
Write-Host ""
Write-Host "⚠️  IMPORTANTE: Si el navegador muestra advertencia de seguridad:" -ForegroundColor Yellow
Write-Host "   1. Haz clic en 'Avanzado'" -ForegroundColor White
Write-Host "   2. Haz clic en 'Continuar a localhost (no seguro)'" -ForegroundColor White
Write-Host "   3. El sitio será seguro con el candado 🔒" -ForegroundColor White
Write-Host ""
Write-Host "📄 PDF mejorado: Generación robusta con múltiples respaldos" -ForegroundColor Cyan
Write-Host "🔧 Presiona Ctrl+C para detener el servidor" -ForegroundColor Yellow
Write-Host ""

# Iniciar servidor
python servidor_seguro_https.py