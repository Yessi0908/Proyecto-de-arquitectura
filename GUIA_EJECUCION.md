# 🌿 Sistema de Invernadero Automatizado IoT

## 📋 Descripción General

Este proyecto implementa un **sistema completo de invernadero automatizado** que combina:
- **Monitoreo ambiental** (temperatura y humedad)
- **Sistema de seguridad** (detectores PIR y de humo)  
- **Control de acceso RFID**
- **Dashboard web en tiempo real**
- **Generación de reportes PDF**

El sistema utiliza **Arduino/ESP32** para la captura de datos, **Flask** como backend, **MySQL** como base de datos y un **dashboard web moderno** para visualización.

## 🛠️ Tecnologías Utilizadas

- **Backend**: Python 3 + Flask
- **Base de Datos**: MySQL 8.0 (Docker)
- **Frontend**: HTML5, CSS3, JavaScript
- **IoT**: Arduino/ESP32 con sensores DHT, MQ-2, PIR, RFID
- **Contenedores**: Docker + Docker Compose
- **Reportes**: ReportLab para generación de PDFs

## 📁 Estructura del Proyecto

```
Proyecto-de-arquitectura/
├── 📄 README.md                    # Este archivo
├── 🐳 docker-compose.yml          # Configuración Docker
├── 🚀 start.ps1                   # Script de inicio Windows
├── 🐧 start.sh                    # Script de inicio Linux/macOS
├── 🧪 test-system.ps1             # Script de pruebas
├── 📚 docs/                       # Documentación
├── 🔧 arduino/                    # Código Arduino/ESP32
│   ├── invernadero_esp32.ino      # Código principal
│   └── README_ARDUINO.md          # Guía Arduino
└── 🖥️ backend/                    # Servidor Flask
    ├── app.py                     # Aplicación principal
    ├── requirements.txt           # Dependencias Python
    ├── Dockerfile                 # Imagen Docker
    ├── pdf_generator.py           # Generador PDF
    └── static/                    # Archivos web
        ├── index.html             # Dashboard principal
        └── estadisticas.html      # Panel estadísticas
```

## 🚀 Guía de Instalación y Ejecución

### 📋 Prerrequisitos

#### Para Windows:
1. **Docker Desktop** - [Descargar aquí](https://www.docker.com/products/docker-desktop)
2. **Windows PowerShell** (incluido en Windows)
3. **Git** (opcional, para clonar el repositorio)

#### Para Linux/macOS:
1. **Docker** y **Docker Compose**
2. **Terminal bash/zsh**
3. **Git** (opcional)

### 🎯 Método 1: Ejecución Automática (Recomendado)

#### En Windows:
```powershell
# 1. Abrir PowerShell como Administrador
# 2. Navegar al directorio del proyecto
cd "ruta\al\Proyecto-de-arquitectura"

# 3. Ejecutar script de inicio
.\start.ps1
```

#### En Linux/macOS:
```bash
# 1. Navegar al directorio del proyecto
cd /ruta/al/Proyecto-de-arquitectura

# 2. Dar permisos al script
chmod +x start.sh

# 3. Ejecutar script de inicio
./start.sh
```

### 🔧 Método 2: Ejecución Manual

#### 1. Verificar Docker
```powershell
# Windows PowerShell
docker --version
docker-compose --version

# Si Docker no está ejecutándose
# Iniciar Docker Desktop manualmente
```

```bash
# Linux/macOS
docker --version
docker-compose --version

# Iniciar Docker si no está ejecutándose
sudo systemctl start docker  # Linux
```

#### 2. Construir y Ejecutar Servicios
```powershell
# Windows - desde el directorio del proyecto
docker-compose down          # Limpiar contenedores previos
docker-compose up --build -d # Construir e iniciar servicios
```

```bash
# Linux/macOS - desde el directorio del proyecto
docker-compose down          # Limpiar contenedores previos
docker-compose up --build -d # Construir e iniciar servicios
```

#### 3. Inicializar Base de Datos
```powershell
# Windows - esperar 30 segundos y ejecutar
Start-Sleep -Seconds 30
Invoke-WebRequest -Uri "http://localhost:5000/api/init" -Method POST -ContentType "application/json" -Body "{}"
```

```bash
# Linux/macOS - esperar 30 segundos y ejecutar
sleep 30
curl -X POST http://localhost:5000/api/init -H "Content-Type: application/json" -d "{}"
```

### 🎯 Método 3: Desarrollo Local (Sin Docker)

#### 1. Instalar MySQL
```bash
# Instalar MySQL Server localmente
# Crear base de datos 'invernadero'
# Usuario: root, Password: root
```

#### 2. Configurar Entorno Python
```powershell
# Windows
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
```

```bash
# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

#### 3. Configurar Variables de Entorno
```powershell
# Windows PowerShell
$env:DB_HOST="localhost"
$env:DB_USER="root"
$env:DB_PASSWORD="root"
$env:DB_NAME="invernadero"
```

```bash
# Linux/macOS
export DB_HOST="localhost"
export DB_USER="root"
export DB_PASSWORD="root"
export DB_NAME="invernadero"
```

#### 4. Ejecutar Aplicación
```powershell
# Windows
python backend\app.py
```

```bash
# Linux/macOS
python backend/app.py
```

## 🌐 Acceso al Sistema

Una vez iniciado el sistema, acceder a:

- **🏠 Dashboard Principal**: http://localhost:5000
- **📊 Panel de Estadísticas**: http://localhost:5000/estadisticas.html
- **📡 API REST**: http://localhost:5000/api/

### 🔗 Endpoints Principales

```
GET  /                          # Dashboard principal
GET  /estadisticas.html         # Panel estadísticas
POST /api/init                  # Inicializar BD
POST /api/ambiente             # Registrar datos ambiente
POST /api/seguridad            # Registrar eventos seguridad
POST /api/acceso               # Registrar accesos RFID
GET  /api/registros            # Obtener registros
GET  /api/estadisticas         # Obtener estadísticas
GET  /api/reporte              # Generar reporte PDF
```

## 🔧 Configuración del Hardware Arduino

### 📡 Conexiones ESP32

```cpp
// Pines de conexión
#define DHT_PIN 4           // Sensor temperatura/humedad
#define PIR_PIN 2           // Detector movimiento
#define MQ2_PIN 34          // Sensor humo (analógico)
#define BOMBA_PIN 5         # Relé bomba agua
#define BUZZER_PIN 18       # Alarma sonora
#define LED_PIN 19          # Indicador LED

// RFID (SPI)
#define RST_PIN 22
#define SS_PIN 21
```

### 📶 Configuración WiFi

Editar en `arduino/invernadero_esp32.ino`:

```cpp
const char* ssid = "TU_WIFI_SSID";
const char* password = "TU_WIFI_PASSWORD";
const char* serverIP = "192.168.1.100";  // IP del servidor
```

### 📤 Subir Código Arduino

1. **Instalar Arduino IDE**
2. **Instalar librerías necesarias**:
   - WiFi
   - HTTPClient  
   - ArduinoJson
   - DHT sensor library
   - MFRC522 (RFID)

3. **Conectar ESP32 y subir código**

## 🧪 Verificación del Sistema

### ✅ Comprobar Servicios

```powershell
# Windows - verificar contenedores
docker ps

# Verificar logs
docker-compose logs backend
docker-compose logs db

# Probar API
Invoke-WebRequest -Uri "http://localhost:5000/api/registros"
```

```bash
# Linux/macOS - verificar contenedores  
docker ps

# Verificar logs
docker-compose logs backend
docker-compose logs db

# Probar API
curl http://localhost:5000/api/registros
```

### 🔍 Script de Pruebas Automáticas

```powershell
# Windows - ejecutar pruebas completas
.\test-system.ps1
```

## 🚨 Solución de Problemas Comunes

### ❌ Docker no responde
```bash
# Reiniciar Docker Desktop
# Verificar recursos de memoria (mínimo 4GB)
# Limpiar contenedores: docker system prune -a
```

### ❌ Error de conexión a base de datos
```bash
# Verificar contenedor MySQL: docker ps
# Verificar logs: docker-compose logs db
# Reiniciar servicios: docker-compose restart
```

### ❌ Puerto 5000 ocupado
```bash
# Windows: netstat -ano | findstr :5000
# Linux: lsof -i :5000
# Cambiar puerto en docker-compose.yml
```

### ❌ Problemas de CORS
- Verificar que `flask-cors` está instalado
- Revisar configuración de red del navegador

## 📊 Funcionalidades del Sistema

### 🌡️ Monitoreo Ambiental
- ✅ Temperatura y humedad en tiempo real
- ✅ Control automático de bomba de agua
- ✅ Alertas por valores fuera de rango
- ✅ Historial de datos ambientales

### 🔒 Sistema de Seguridad  
- ✅ Detector de movimiento PIR
- ✅ Sensor de humo MQ-2
- ✅ Alertas visuales y sonoras
- ✅ Registro de eventos de seguridad

### 🔑 Control de Acceso
- ✅ Lectores RFID
- ✅ Registro de entrada/salida
- ✅ Control de usuarios autorizados
- ✅ Alertas de acceso no autorizado

### 📈 Dashboard Web
- ✅ Visualización en tiempo real
- ✅ Gráficos dinámicos
- ✅ Filtros por fecha y tipo
- ✅ Exportación de reportes PDF
- ✅ Interfaz responsive

## 📄 Generación de Reportes

El sistema incluye múltiples generadores de PDF:

```bash
# Acceder a reportes
GET http://localhost:5000/api/reporte?fecha_inicio=2024-01-01&fecha_fin=2024-12-31
```

### 📋 Tipos de Reporte
- **📊 Reporte Completo**: Todos los datos del período
- **🌡️ Reporte Ambiental**: Solo datos de temperatura/humedad  
- **🔒 Reporte de Seguridad**: Solo eventos de seguridad
- **🔑 Reporte de Accesos**: Solo registros RFID

## 🔄 Mantenimiento

### 🧹 Limpieza de Datos
```sql
-- Limpiar registros antiguos (opcional)
DELETE FROM registros_ambiente WHERE fecha < DATE_SUB(NOW(), INTERVAL 30 DAY);
DELETE FROM registros_seguridad WHERE fecha < DATE_SUB(NOW(), INTERVAL 30 DAY);
DELETE FROM registros_acceso WHERE fecha < DATE_SUB(NOW(), INTERVAL 30 DAY);
```

### 💾 Backup de Base de Datos
```bash
# Crear backup
docker exec invernadero_db mysqldump -u root -proot invernadero > backup_$(date +%Y%m%d).sql

# Restaurar backup
docker exec -i invernadero_db mysql -u root -proot invernadero < backup_20241023.sql
```

## 🤝 Contribuir

1. **Fork** el repositorio
2. **Crear** rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. **Push** a la rama (`git push origin feature/nueva-funcionalidad`)
5. **Crear** Pull Request

## 📞 Soporte

- **📧 Email**: soporte@invernadero-iot.com
- **📚 Documentación**: [docs/](./docs/)
- **🐛 Issues**: Crear issue en GitHub
- **💬 Discusiones**: Pestaña Discussions del repositorio

## 📋 Changelog

### v1.0.0 (2024-10-23)
- ✅ Sistema completo implementado
- ✅ Dashboard web funcional
- ✅ Integración Arduino/ESP32
- ✅ Generación de reportes PDF
- ✅ Sistema de alertas
- ✅ Control de acceso RFID

---

## 🎯 Inicio Rápido (Resumen)

```powershell
# Windows - Ejecución en 3 pasos
git clone <repositorio>
cd Proyecto-de-arquitectura
.\start.ps1
# Acceder a http://localhost:5000
```

```bash
# Linux/macOS - Ejecución en 3 pasos  
git clone <repositorio>
cd Proyecto-de-arquitectura
./start.sh
# Acceder a http://localhost:5000
```

**¡El sistema estará listo en menos de 5 minutos!** 🚀

---

*Sistema desarrollado para monitoreo y automatización de invernaderos con tecnología IoT.*