# 🔧 Guía de Solución de Problemas Automática
# Sistema de Invernadero IoT

## 🚨 PROBLEMAS COMUNES Y SOLUCIONES

### **PROBLEMA: Docker no funciona**

**Síntomas:**
- "docker daemon is not running"
- "The system cannot find the file specified"

**Soluciones automáticas:**
1. **Windows**: Ejecutar `start.ps1` como administrador
2. **Linux/Mac**: Ejecutar `chmod +x start.sh && ./start.sh`

**Soluciones manuales:**
```powershell
# Windows - Iniciar Docker Desktop
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
Start-Sleep 30
docker-compose up -d
```

---

### **PROBLEMA: Puerto 5000 ocupado**

**Síntomas:**
- "Port 5000 is already in use"
- Error al iniciar backend

**Solución automática:**
```powershell
# Encontrar y terminar proceso en puerto 5000
$process = Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue
if ($process) {
    Stop-Process -Id $process.OwningProcess -Force
}
docker-compose up -d
```

**Solución alternativa:**
```yaml
# En docker-compose.yml cambiar:
ports:
  - "8080:5000"  # Usar puerto 8080 en lugar de 5000
```

---

### **PROBLEMA: Error de importación Python**

**Síntomas:**
- "La importación no se ha podido resolver"
- Errores de linting en VS Code

**Solución:**
Los errores son solo de linting local. El sistema funciona correctamente en Docker.

**Para desarrollo local (opcional):**
```bash
pip install flask flask-cors pymysql reportlab
```

---

### **PROBLEMA: Base de datos no conecta**

**Síntomas:**
- "Cannot connect to DB"
- Error 500 en API

**Diagnóstico automático:**
```powershell
# Verificar estado de contenedores
docker-compose ps

# Ver logs de MySQL
docker-compose logs db

# Reiniciar solo la base de datos
docker-compose restart db
```

**Solución:**
```powershell
# Reset completo de base de datos
docker-compose down -v
docker-compose up -d
Start-Sleep 20
Invoke-RestMethod -Uri "http://localhost:5000/api/init" -Method POST
```

---

### **PROBLEMA: Arduino no envía datos**

**Diagnóstico:**
1. **Verificar WiFi:** Monitor Serie debe mostrar "WiFi conectado"
2. **Verificar IP:** Cambiar IP en código Arduino por IP real del servidor
3. **Verificar firewall:** Permitir puerto 5000

**Test manual:**
```powershell
# Simular datos de Arduino
$body = @{
    temperatura = 25.5
    humedad = 60.2
    estado_bomba = "Apagada"
    alerta = "Normal"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/sensores/ambiente" -Method POST -Body $body -ContentType "application/json"
```

---

### **PROBLEMA: Dashboard no carga datos**

**Diagnóstico automático:**
```powershell
# Test de API endpoints
$endpoints = @(
    "http://localhost:5000/api/estado/actual",
    "http://localhost:5000/api/ambiente",
    "http://localhost:5000/api/estadisticas"
)

foreach ($endpoint in $endpoints) {
    try {
        $response = Invoke-RestMethod -Uri $endpoint
        Write-Host "✅ $endpoint - OK" -ForegroundColor Green
    } catch {
        Write-Host "❌ $endpoint - Error: $($_.Exception.Message)" -ForegroundColor Red
    }
}
```

**Soluciones:**
1. **Limpiar caché del navegador:** Ctrl+F5
2. **Verificar consola:** F12 → Console → Buscar errores
3. **Reiniciar backend:**
```powershell
docker-compose restart backend
```

---

### **PROBLEMA: Reportes PDF no funcionan**

**Síntomas:**
- "Función PDF no disponible"
- Error 503 al descargar PDF

**Causa:** ReportLab no instalado localmente (normal)

**Solución:** Usar Docker:
```powershell
# Acceder dentro del contenedor y generar reporte
docker-compose exec backend python -c "
import requests
r = requests.get('http://localhost:5000/api/report')
with open('/tmp/reporte.pdf', 'wb') as f: f.write(r.content)
"
```

---

## 🚀 SCRIPT DE DIAGNÓSTICO AUTOMÁTICO

```powershell
# Ejecutar este script para diagnóstico completo
Write-Host "🔍 Ejecutando diagnóstico del sistema..." -ForegroundColor Cyan

# 1. Verificar Docker
try { docker --version; Write-Host "✅ Docker OK" } 
catch { Write-Host "❌ Docker no disponible" }

# 2. Verificar contenedores
docker-compose ps

# 3. Test de conectividad
$tests = @{
    "Frontend" = "http://localhost:5000"
    "API Estado" = "http://localhost:5000/api/estado/actual"
    "API Ambiente" = "http://localhost:5000/api/ambiente"
}

foreach ($test in $tests.GetEnumerator()) {
    try {
        Invoke-WebRequest $test.Value -UseBasicParsing | Out-Null
        Write-Host "✅ $($test.Key)" -ForegroundColor Green
    } catch {
        Write-Host "❌ $($test.Key)" -ForegroundColor Red
    }
}

# 4. Verificar logs por errores
Write-Host "`n🔍 Últimos errores en logs:"
docker-compose logs --tail=10 backend | Select-String "ERROR|Exception"

Write-Host "`n🎯 Diagnóstico completado" -ForegroundColor Green
```

---

## 📞 SOLUCIÓN RÁPIDA - COMANDO DE EMERGENCIA

```powershell
# RESET COMPLETO DEL SISTEMA
Write-Host "🚨 Ejecutando reset completo..." -ForegroundColor Red

# Parar todo
docker-compose down -v
docker system prune -f

# Esperar
Start-Sleep 10

# Reiniciar todo
docker-compose up --build -d
Start-Sleep 30

# Verificar
docker-compose ps
Invoke-WebRequest "http://localhost:5000" -UseBasicParsing

Write-Host "✅ Reset completado" -ForegroundColor Green
```

---

## ❓ FAQ RÁPIDO

**P: ¿Por qué hay errores rojos en VS Code?**
R: Son errores de linting. El sistema funciona en Docker. Ignorar o instalar librerías localmente.

**P: ¿Cómo cambiar el puerto 5000?**
R: Modificar `ports: - "NUEVO_PUERTO:5000"` en docker-compose.yml

**P: ¿El Arduino es obligatorio?**
R: No. El sistema funciona sin hardware. Usar datos simulados para pruebas.

**P: ¿Cómo hacer backup?**
R: `docker-compose exec db mysqldump -u root -p invernadero > backup.sql`

**P: ¿Funciona en Raspberry Pi?**
R: Sí, cambiar imagen base a `FROM python:3.11-slim-arm64` en Dockerfile.

---

**🆘 Si nada funciona:** 
1. Reiniciar Docker Desktop
2. Ejecutar `start.ps1` como administrador
3. Verificar que no haya antivirus bloqueando puertos
4. Usar puertos alternativos (8080, 3000, etc.)