# 🌿 SISTEMA INVERNADERO - MODO ARDUINO REAL

## ✅ ESTADO ACTUAL: LISTO PARA ARDUINO ESP32

El sistema está **completamente configurado** para recibir datos reales del Arduino ESP32, **SIN SIMULACIÓN**.

---

## 🚀 SERVIDOR ACTIVO

**URL del Servidor:** `http://192.168.1.7:5000`

- 📊 **Dashboard:** http://192.168.1.7:5000
- 🔧 **Configuración:** http://192.168.1.7:5000/config  
- 📡 **API Health:** http://192.168.1.7:5000/api/health
- 🎯 **Endpoint Arduino:** `POST http://192.168.1.7:5000/api/sensores/ambiente`

---

## ⚙️ CONFIGURACIÓN DEL ARDUINO ESP32

### 1. 📝 Editar el archivo Arduino

Abrir: `arduino/invernadero_esp32.ino`

Buscar las líneas (aproximadamente línea 31-33):
```cpp
const char* ssid = "TU_WIFI_SSID";           
const char* password = "TU_WIFI_PASSWORD";    
const char* serverURL = "http://192.168.1.100:5000";
```

### 2. 🔧 Cambiar por tu configuración:
```cpp
const char* ssid = "TU_RED_WIFI_REAL";           // ⚠️ CAMBIAR
const char* password = "TU_PASSWORD_REAL";       // ⚠️ CAMBIAR  
const char* serverURL = "http://192.168.1.7:5000";  // ✅ YA CONFIGURADO
```

### 3. 📤 Compilar y Subir al Arduino

1. Conectar Arduino ESP32 al USB
2. Seleccionar puerto COM correcto  
3. Compilar y subir el código
4. Abrir monitor serie (115200 baud)

---

## 🔍 VALIDACIÓN DEL FUNCIONAMIENTO

### En el Monitor Serie del Arduino:
```
✅ Sistema iniciado correctamente
📡 Monitoreando sensores...
🔗 Conectando a WiFi...
📤 Datos enviados correctamente
```

### En el Dashboard Web:
- Estado cambia de `⏳ Esperando datos...` a `✅ Arduino Conectado`
- Aparecen valores reales de temperatura y humedad
- Gráficos se actualizan automáticamente cada 30 segundos
- Estadísticas muestran registros del Arduino

---

## 📊 DATOS QUE ENVÍA EL ARDUINO

El Arduino enviará cada 30 segundos:

```json
{
  "temperatura": 24.5,
  "humedad": 65.2, 
  "estado_bomba": "Encendida",
  "alerta": "Normal"
}
```

**Rangos válidos:**
- 🌡️ Temperatura: -50°C a 100°C
- 💧 Humedad: 0% a 100%
- 💡 Estado bomba: "Encendida" / "Apagada"
- 🚨 Alerta: "Normal" / "Medio" / "Alto" / "Crítico"

---

## 🧪 PRUEBAS SIN ARDUINO

Si quieres probar el sistema antes de conectar el Arduino:

```powershell
python test_arduino_simulator.py
```

Este script simula el comportamiento del Arduino ESP32 real.

---

## 🔧 SOLUCIÓN DE PROBLEMAS

### ❌ Arduino no conecta a WiFi
1. Verificar nombre de red WiFi (SSID)
2. Verificar contraseña WiFi
3. Asegurar que WiFi sea 2.4GHz (no 5GHz)
4. Verificar señal WiFi fuerte

### ❌ No aparecen datos en Dashboard  
1. Verificar IP del servidor: `192.168.1.7:5000`
2. Revisar monitor serie del Arduino
3. Comprobar que no hay firewall bloqueando puerto 5000
4. Verificar que la base de datos MySQL esté activa

### ❌ Error "Base de datos desconectada"
```powershell
# Iniciar MySQL (si está instalado localmente)
net start mysql

# O usar XAMPP/WAMP si tienes instalado
```

---

## 📁 ARCHIVOS DEL SISTEMA

```
📂 Proyecto-de-arquitectura/
├── 🐍 servidor_arduino_real.py         ← Servidor Flask principal
├── 📋 CONFIGURACION_ARDUINO.txt        ← Configuración detallada
├── 🧪 test_arduino_simulator.py        ← Simulador para pruebas
├── 📊 setup_database.py                ← Configuración de base de datos
└── 📂 arduino/
    └── 🔧 invernadero_esp32.ino        ← Código para el Arduino
```

---

## 🎯 SIGUIENTE PASO

1. **Configurar Arduino** con tu WiFi real
2. **Compilar y subir** el código al ESP32
3. **Abrir dashboard** en http://192.168.1.7:5000
4. **Verificar** que aparezcan datos reales

¡El sistema está **100% listo** para datos reales! 🌱✨