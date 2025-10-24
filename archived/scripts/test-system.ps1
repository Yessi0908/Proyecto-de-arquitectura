# Test Completo del Sistema de Invernadero IoT
# Verificación de todas las funcionalidades

Write-Host "🧪 Iniciando pruebas del Sistema de Invernadero..." -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan

$errors = 0
$tests = 0

function Test-Endpoint {
    param($Name, $Uri, $Method = "GET", $Body = $null)
    
    $tests++
    try {
        if ($Method -eq "GET") {
            $result = Invoke-RestMethod -Uri $Uri -ErrorAction Stop
        } else {
            $result = Invoke-RestMethod -Uri $Uri -Method $Method -Body $Body -ContentType "application/json" -ErrorAction Stop
        }
        Write-Host "✅ $Name" -ForegroundColor Green
        return $result
    } catch {
        Write-Host "❌ $Name - Error: $($_.Exception.Message)" -ForegroundColor Red
        $script:errors++
        return $null
    }
}

# 1. Verificar servicios básicos
Write-Host "`n🔍 Verificando servicios básicos..." -ForegroundColor Yellow

Test-Endpoint "Dashboard Principal" "http://localhost:5000"
Test-Endpoint "Página de Estadísticas" "http://localhost:5000/static/estadisticas.html"

# 2. Verificar APIs de consulta
Write-Host "`n📊 Verificando APIs de consulta..." -ForegroundColor Yellow

Test-Endpoint "Estado Actual" "http://localhost:5000/api/estado/actual"
Test-Endpoint "Datos Ambientales" "http://localhost:5000/api/ambiente"
Test-Endpoint "Eventos de Seguridad" "http://localhost:5000/api/seguridad"
Test-Endpoint "Registros de Acceso" "http://localhost:5000/api/accesos"
Test-Endpoint "Estadísticas" "http://localhost:5000/api/estadisticas"
Test-Endpoint "Alertas del Sistema" "http://localhost:5000/api/alertas/sistema"
Test-Endpoint "Configuración de Umbrales" "http://localhost:5000/api/config/umbrales"

# 3. Verificar APIs de inserción
Write-Host "`n📝 Verificando APIs de inserción..." -ForegroundColor Yellow

# Datos ambientales
$ambienteData = @{
    temperatura = 28.5
    humedad = 45.0
    estado_bomba = "Encendida"
    alerta = "Alto"
} | ConvertTo-Json

Test-Endpoint "Insertar Ambiente" "http://localhost:5000/api/sensores/ambiente" "POST" $ambienteData

# Datos de seguridad
$seguridadData = @{
    tipo_evento = "Humo"
    descripcion = "Nivel elevado detectado: 350"
    nivel_alerta = "Alto"
} | ConvertTo-Json

Test-Endpoint "Insertar Seguridad" "http://localhost:5000/api/sensores/seguridad" "POST" $seguridadData

# Datos de acceso (simplificado)
$accesoData = @{
    id_tarjeta = "12345678"
    persona = "Usuario Test"
    acceso_autorizado = $true
    temperatura = 26.0
    humedad = 55.0
} | ConvertTo-Json

Test-Endpoint "Insertar Acceso" "http://localhost:5000/api/sensores/acceso" "POST" $accesoData

# 4. Verificar datos después de inserción
Write-Host "`n🔄 Verificando datos actualizados..." -ForegroundColor Yellow

$estadoActual = Test-Endpoint "Estado Después de Inserciones" "http://localhost:5000/api/estado/actual"

if ($estadoActual) {
    Write-Host "`n📋 Datos actuales:" -ForegroundColor Cyan
    if ($estadoActual.ambiente) {
        Write-Host "   🌡️  Temperatura: $($estadoActual.ambiente.temperatura)°C" -ForegroundColor White
        Write-Host "   💧 Humedad: $($estadoActual.ambiente.humedad)%" -ForegroundColor White
        Write-Host "   💦 Bomba: $($estadoActual.ambiente.estado_bomba)" -ForegroundColor White
    }
    if ($estadoActual.eventos) {
        Write-Host "   📊 Eventos registrados: $($estadoActual.eventos.Count)" -ForegroundColor White
    }
}

# 5. Test de funcionalidades avanzadas
Write-Host "`n🚀 Verificando funcionalidades avanzadas..." -ForegroundColor Yellow

# Test de filtros con fechas
$fechaHoy = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ss")
$fechaAyer = (Get-Date).AddDays(-1).ToString("yyyy-MM-ddTHH:mm:ss")

Test-Endpoint "Filtro por Fechas" "http://localhost:5000/api/ambiente?desde=$fechaAyer&hasta=$fechaHoy"

# Test de configuración de umbrales
$umbralData = @{
    temperatura = @{
        min = 20.0
        max = 30.0
        critica = 40.0
    }
    humedad = @{
        min = 35.0
        max = 75.0
    }
} | ConvertTo-Json -Depth 3

Test-Endpoint "Actualizar Umbrales" "http://localhost:5000/api/config/umbrales" "POST" $umbralData

# 6. Resumen de resultados
Write-Host "`n" + "="*50 -ForegroundColor Cyan
Write-Host "📊 RESUMEN DE PRUEBAS" -ForegroundColor Cyan
Write-Host "="*50 -ForegroundColor Cyan

if ($errors -eq 0) {
    Write-Host "🎉 ¡TODAS LAS PRUEBAS EXITOSAS!" -ForegroundColor Green
    Write-Host "✅ $tests/$tests pruebas completadas correctamente" -ForegroundColor Green
    Write-Host ""
    Write-Host "🌐 Sistema funcionando perfectamente en:" -ForegroundColor Cyan
    Write-Host "   Dashboard: http://localhost:5000" -ForegroundColor White
    Write-Host "   Estadísticas: http://localhost:5000/static/estadisticas.html" -ForegroundColor White
    Write-Host ""
    Write-Host "🤖 Para conectar Arduino, revisar:" -ForegroundColor Cyan
    Write-Host "   /arduino/README_ARDUINO.md" -ForegroundColor White
} else {
    Write-Host "⚠️  Algunos tests fallaron: $errors/$tests" -ForegroundColor Yellow
    Write-Host "🔧 Revisar logs con: docker-compose logs" -ForegroundColor Yellow
}

Write-Host "`n🎯 Sistema de Invernadero IoT - Test Completado" -ForegroundColor Green