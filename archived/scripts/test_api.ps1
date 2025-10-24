# Script PowerShell para probar la API del invernadero
Write-Host "🧪 Probando la API del invernadero con PowerShell..." -ForegroundColor Green

# Probar salud de la API
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000/api/health" -Method GET -UseBasicParsing
    Write-Host "✅ API Health - Status: $($response.StatusCode)" -ForegroundColor Green
    $data = $response.Content | ConvertFrom-Json
    Write-Host "   Mensaje: $($data.message)" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Error en health check: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Probar estado actual
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000/api/estado/actual" -Method GET -UseBasicParsing
    Write-Host "✅ Estado Actual - Status: $($response.StatusCode)" -ForegroundColor Green
    $data = $response.Content | ConvertFrom-Json
    $temp = if ($data.ambiente.temperatura) { $data.ambiente.temperatura } else { "N/A" }
    $hum = if ($data.ambiente.humedad) { $data.ambiente.humedad } else { "N/A" }
    Write-Host "   Ambiente: Temp: ${temp}°C, Hum: ${hum}%" -ForegroundColor Cyan
    Write-Host "   Eventos registrados: $($data.eventos.Count)" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Error obteniendo estado actual: $($_.Exception.Message)" -ForegroundColor Red
}

# Simular nuevos datos
try {
    $body = "{}" 
    $response = Invoke-WebRequest -Uri "http://localhost:5000/api/simular_datos" -Method POST -Body $body -ContentType "application/json" -UseBasicParsing
    Write-Host "✅ Simulación de datos - Status: $($response.StatusCode)" -ForegroundColor Green
    $data = $response.Content | ConvertFrom-Json
    $temp = $data.nuevo_registro.temperatura
    $hum = $data.nuevo_registro.humedad
    Write-Host "   Nuevos datos: Temp: ${temp}°C, Hum: ${hum}%" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Error simulando datos: $($_.Exception.Message)" -ForegroundColor Red
}

# Verificar datos de ambiente
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000/api/ambiente?limit=3" -Method GET -UseBasicParsing
    Write-Host "✅ API Ambiente - Status: $($response.StatusCode)" -ForegroundColor Green
    $data = $response.Content | ConvertFrom-Json
    Write-Host "   Registros encontrados: $($data.Count)" -ForegroundColor Cyan
    for ($i = 0; $i -lt [Math]::Min(3, $data.Count); $i++) {
        $registro = $data[$i]
        Write-Host "   $($i+1). Fecha: $($registro.fecha), Temp: $($registro.temperatura)°C, Hum: $($registro.humedad)%" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Error obteniendo ambiente: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "🔥 Prueba finalizada - Ahora revisa la interfaz web en http://localhost:5000" -ForegroundColor Green
Write-Host "📊 La interfaz debería mostrar los datos de temperatura y humedad" -ForegroundColor Green