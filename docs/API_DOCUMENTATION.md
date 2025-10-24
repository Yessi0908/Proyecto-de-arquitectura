5# 🔧 Documentación Técnica de la API
# Sistema de Invernadero Automatizado

## 📡 **Endpoints de la API REST**

**Base URL**: `http://localhost:5000/api`

---

## 🛠️ **Endpoints de Inicialización**

### **POST /api/init**
Inicializa las tablas de la base de datos.

**Request:**
```json
{}
```

**Response:**
```json
{
    "status": "ok"
}
```

**Códigos de estado:**
- `201`: Creado exitosamente
- `500`: Error interno del servidor

---

## 🌡️ **Endpoints de Sensores Ambientales**

### **POST /api/sensores/ambiente**
Registra datos de temperatura, humedad y estado de bomba.

**Request:**
```json
{
    "temperatura": 25.6,
    "humedad": 65.2,
    "estado_bomba": "Encendida",
    "alerta": "Normal"
}
```

**Campos:**
- `temperatura` (float): Temperatura en °C
- `humedad` (float): Humedad relativa en %
- `estado_bomba` (string): "Encendida" o "Apagada"
- `alerta` (string, opcional): Nivel de alerta ("Normal", "Medio", "Alto", "Crítico")

**Response:**
```json
{
    "status": "ok"
}
```

### **GET /api/ambiente**
Obtiene registros de datos ambientales.

**Parámetros de query:**
- `desde` (datetime, opcional): Fecha inicio (ISO format)
- `hasta` (datetime, opcional): Fecha fin (ISO format)

**Request:**
```
GET /api/ambiente?desde=2025-10-19T00:00:00&hasta=2025-10-20T23:59:59
```

**Response:**
```json
[
    {
        "id": 1,
        "fecha": "2025-10-20T14:30:00",
        "temperatura": 25.6,
        "humedad": 65.2,
        "estado_bomba": "Encendida",
        "alerta": "Normal"
    }
]
```

---

## 🚨 **Endpoints de Seguridad**

### **POST /api/sensores/seguridad**
Registra eventos de seguridad (movimiento, humo, etc.).

**Request:**
```json
{
    "tipo_evento": "Movimiento",
    "descripcion": "Actividad detectada en zona norte",
    "nivel_alerta": "Medio"
}
```

**Campos:**
- `tipo_evento` (string): "Movimiento", "Humo", etc.
- `descripcion` (string): Descripción detallada del evento
- `nivel_alerta` (string): "Bajo", "Medio", "Alto", "Crítico"

**Response:**
```json
{
    "status": "ok"
}
```

### **GET /api/seguridad**
Obtiene registros de eventos de seguridad.

**Parámetros de query:**
- `desde` (datetime, opcional): Fecha inicio
- `hasta` (datetime, opcional): Fecha fin

**Response:**
```json
[
    {
        "id": 1,
        "fecha": "2025-10-20T14:35:00",
        "tipo_evento": "Movimiento",
        "descripcion": "Actividad detectada en zona norte",
        "nivel_alerta": "Medio"
    }
]
```

---

## 🪪 **Endpoints de Control de Acceso**

### **POST /api/sensores/acceso**
Registra intentos de acceso RFID.

**Request:**
```json
{
    "id_tarjeta": "AB12CD34",
    "persona": "Juan Pérez",
    "estado_bomba": "Apagada",
    "temperatura": 24.1,
    "humedad": 58.3,
    "acceso_autorizado": true,
    "observacion": "Acceso normal"
}
```

**Campos:**
- `id_tarjeta` (string): ID único de la tarjeta RFID
- `persona` (string): Nombre de la persona (si está registrada)
- `estado_bomba` (string): Estado de la bomba al momento del acceso
- `temperatura` (float): Temperatura al momento del acceso
- `humedad` (float): Humedad al momento del acceso
- `acceso_autorizado` (boolean): true si es acceso válido
- `observacion` (string, opcional): Notas adicionales

**Response:**
```json
{
    "status": "ok"
}
```

### **GET /api/accesos**
Obtiene registros de accesos.

**Parámetros de query:**
- `desde` (datetime, opcional): Fecha inicio
- `hasta` (datetime, opcional): Fecha fin

**Response:**
```json
[
    {
        "id": 1,
        "fecha": "2025-10-20T14:20:00",
        "id_tarjeta": "AB12CD34",
        "persona": "Juan Pérez",
        "estado_bomba": "Apagada",
        "temperatura": 24.1,
        "humedad": 58.3,
        "acceso_autorizado": true,
        "observacion": "Acceso normal"
    }
]
```

---

## 📊 **Endpoints de Estado y Estadísticas**

### **GET /api/estado/actual**
Obtiene el estado actual de todos los módulos del sistema.

**Response:**
```json
{
    "ambiente": {
        "id": 1,
        "fecha": "2025-10-20T14:30:00",
        "temperatura": 25.6,
        "humedad": 65.2,
        "estado_bomba": "Encendida",
        "alerta": "Normal"
    },
    "seguridad": {
        "id": 1,
        "fecha": "2025-10-20T14:35:00",
        "tipo_evento": "Movimiento",
        "descripcion": "Actividad detectada",
        "nivel_alerta": "Medio"
    },
    "acceso": {
        "id": 1,
        "fecha": "2025-10-20T14:20:00",
        "persona": "Juan Pérez",
        "acceso_autorizado": true
    },
    "eventos": [
        {
            "fecha": "2025-10-20T14:35:00",
            "tipo": "Movimiento",
            "descripcion": "Actividad detectada",
            "nivel": "Medio"
        }
    ]
}
```

### **GET /api/estadisticas**
Obtiene estadísticas del sistema para un período específico.

**Parámetros de query:**
- `desde` (datetime, opcional): Fecha inicio (default: 7 días atrás)
- `hasta` (datetime, opcional): Fecha fin (default: ahora)

**Response:**
```json
{
    "ambiente": {
        "total_registros": 1440,
        "temp_promedio": 24.5,
        "temp_minima": 18.2,
        "temp_maxima": 32.1,
        "hum_promedio": 62.3,
        "hum_minima": 35.0,
        "hum_maxima": 85.5,
        "activaciones_bomba": 45
    },
    "seguridad": {
        "total_eventos": 12,
        "eventos_movimiento": 8,
        "eventos_humo": 1,
        "alertas_criticas": 0,
        "alertas_altas": 2
    },
    "acceso": {
        "total_accesos": 15,
        "accesos_autorizados": 14,
        "accesos_denegados": 1
    },
    "periodo": {
        "desde": "2025-10-13T14:30:00",
        "hasta": "2025-10-20T14:30:00"
    }
}
```

### **GET /api/alertas/sistema**
Obtiene alertas activas del sistema basadas en umbrales.

**Response:**
```json
{
    "alertas": [
        {
            "tipo": "Temperatura",
            "nivel": "Alto",
            "mensaje": "Temperatura fuera de rango: 32.5°C",
            "fecha": "2025-10-20T14:30:00"
        }
    ],
    "total": 1,
    "criticas": 0,
    "altas": 1
}
```

---

## ⚙️ **Endpoints de Configuración**

### **GET /api/config/umbrales**
Obtiene la configuración actual de umbrales.

**Response:**
```json
{
    "temperatura": {
        "min": 18.0,
        "max": 28.0,
        "critica": 35.0
    },
    "humedad": {
        "min": 40.0,
        "max": 70.0,
        "critica_baja": 30.0,
        "critica_alta": 80.0
    },
    "humo": {
        "umbral": 300,
        "critico": 500
    }
}
```

### **POST /api/config/umbrales**
Actualiza la configuración de umbrales.

**Request:**
```json
{
    "temperatura": {
        "min": 16.0,
        "max": 30.0,
        "critica": 38.0
    },
    "humedad": {
        "min": 35.0,
        "max": 75.0,
        "critica_baja": 25.0,
        "critica_alta": 85.0
    },
    "humo": {
        "umbral": 250,
        "critico": 450
    }
}
```

**Response:**
```json
{
    "status": "ok",
    "message": "Umbrales actualizados"
}
```

---

## 📄 **Endpoints de Reportes**

### **GET /api/report**
Genera y descarga un reporte PDF profesional del sistema con estadísticas completas.

**✨ Características del Reporte:**
- 🎨 Diseño profesional con colores y estilos
- 📊 Resumen ejecutivo con estadísticas calculadas
- 📋 Tabla detallada de registros ambientales
- 🔢 Análisis de temperatura y humedad (min, max, promedio)
- 💧 Conteo de activaciones del sistema de riego
- 📅 Información de período y metadata del sistema

**Parámetros de query:**
- `desde` (datetime, opcional): Fecha inicio para filtrar datos
- `hasta` (datetime, opcional): Fecha fin para filtrar datos

**Request:**
```
GET /api/report?desde=2025-10-19T00:00:00&hasta=2025-10-20T23:59:59
```

**Response:**
- Content-Type: `application/pdf`
- Content-Disposition: `attachment; filename="reporte_invernadero_detallado.pdf"`
- Tamaño: A4, diseño optimizado para impresión

**Estructura del PDF:**
1. 🌿 Encabezado con título e información del sistema
2. 📊 Resumen ejecutivo con métricas clave
3. 📋 Tabla detallada de hasta 50 registros más recientes
4. 📄 Pie de página con información del sistema

---

## 🗄️ **Estructura de Base de Datos**

### **Tabla: registros_ambiente**
```sql
CREATE TABLE registros_ambiente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    temperatura FLOAT,
    humedad FLOAT,
    estado_bomba VARCHAR(15),
    alerta VARCHAR(50)
);
```

### **Tabla: registros_seguridad**
```sql
CREATE TABLE registros_seguridad (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    tipo_evento VARCHAR(50),
    descripcion TEXT,
    nivel_alerta VARCHAR(10)
);
```

### **Tabla: registros_acceso**
```sql
CREATE TABLE registros_acceso (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    id_tarjeta VARCHAR(50),
    persona VARCHAR(100),
    estado_bomba VARCHAR(15),
    temperatura FLOAT,
    humedad FLOAT,
    acceso_autorizado BOOLEAN,
    observacion TEXT
);
```

---

## 🔧 **Códigos de Estado HTTP**

- `200`: OK - Solicitud exitosa
- `201`: Created - Recurso creado exitosamente
- `400`: Bad Request - Solicitud malformada
- `404`: Not Found - Endpoint no encontrado
- `500`: Internal Server Error - Error del servidor

---

## 📝 **Ejemplos de Uso con cURL**

### **Inicializar sistema:**
```bash
curl -X POST http://localhost:5000/api/init \
  -H "Content-Type: application/json" \
  -d "{}"
```

### **Enviar datos ambientales:**
```bash
curl -X POST http://localhost:5000/api/sensores/ambiente \
  -H "Content-Type: application/json" \
  -d '{
    "temperatura": 25.6,
    "humedad": 65.2,
    "estado_bomba": "Encendida",
    "alerta": "Normal"
  }'
```

### **Registrar evento de seguridad:**
```bash
curl -X POST http://localhost:5000/api/sensores/seguridad \
  -H "Content-Type: application/json" \
  -d '{
    "tipo_evento": "Humo",
    "descripcion": "Nivel crítico detectado: 520",
    "nivel_alerta": "Crítico"
  }'
```

### **Registrar acceso RFID:**
```bash
curl -X POST http://localhost:5000/api/sensores/acceso \
  -H "Content-Type: application/json" \
  -d '{
    "id_tarjeta": "AB12CD34",
    "persona": "Juan Pérez",
    "estado_bomba": "Apagada",
    "temperatura": 24.1,
    "humedad": 58.3,
    "acceso_autorizado": true,
    "observacion": "Acceso normal"
  }'
```

### **Obtener estado actual:**
```bash
curl http://localhost:5000/api/estado/actual
```

### **Obtener estadísticas:**
```bash
curl "http://localhost:5000/api/estadisticas?desde=2025-10-19T00:00:00&hasta=2025-10-20T23:59:59"
```

---

## 🚀 **Integración con Arduino/ESP32**

### **Librerías requeridas:**
```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
```

### **Función de envío genérica:**
```cpp
void enviarDatosAPI(String endpoint, String jsonData) {
    HTTPClient http;
    http.begin(serverURL + endpoint);
    http.addHeader("Content-Type", "application/json");
    
    int httpCode = http.POST(jsonData);
    if (httpCode == 201) {
        Serial.println("✅ Datos enviados: " + endpoint);
    } else {
        Serial.println("❌ Error: " + String(httpCode));
    }
    http.end();
}
```

---

## 🛡️ **Consideraciones de Seguridad**

### **Headers de seguridad recomendados:**
```python
# En producción agregar:
@app.after_request
def after_request(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response
```

### **Autenticación (implementación futura):**
```python
# JWT Token authentication
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

@app.route('/api/login', methods=['POST'])
def login():
    # Implementar lógica de autenticación
    access_token = create_access_token(identity=username)
    return jsonify({'access_token': access_token})

@app.route('/api/sensores/ambiente', methods=['POST'])
@jwt_required()
def post_ambiente():
    # Endpoint protegido
    pass
```

### **Rate Limiting:**
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@app.route('/api/sensores/ambiente', methods=['POST'])
@limiter.limit("10 per minute")
def post_ambiente():
    # Limitado a 10 requests por minuto
    pass
```

---

## 📊 **Monitoreo y Logging**

### **Logs de aplicación:**
```python
import logging

logging.basicConfig(
    filename='invernadero.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

@app.route('/api/sensores/ambiente', methods=['POST'])
def post_ambiente():
    app.logger.info(f"Datos recibidos: {request.get_json()}")
    # Resto del código
```

### **Métricas de rendimiento:**
- Tiempo de respuesta promedio de APIs
- Número de requests por minuto
- Errores de conexión a base de datos
- Uptime del sistema

---

## 🔄 **Versionado de API**

Para futuras versiones, considerar:
```
/api/v1/sensores/ambiente  # Versión 1
/api/v2/sensores/ambiente  # Versión 2 con nuevas funcionalidades
```

---

**Esta documentación técnica cubre todos los aspectos de la API REST del sistema de invernadero automatizado. Para implementaciones específicas o personalizaciones, contactar al equipo de desarrollo.**