# 🔧 Configuración del Arduino/ESP32

## 📋 **Componentes Necesarios**

### **Microcontrolador:**
- ESP32 DevKit v1 (recomendado) o Arduino UNO + ESP8266

### **Sensores:**
- DHT22 - Sensor de temperatura y humedad
- MQ-2 - Sensor de humo/gas
- PIR HC-SR501 - Sensor de movimiento
- MFRC522 - Módulo RFID

### **Actuadores:**
- Relé de 5V (para control de bomba)
- Bomba de agua 12V
- Buzzer activo 5V
- LEDs: Verde, Amarillo, Rojo

### **Otros:**
- Resistencias: 220Ω (3x para LEDs)
- Protoboard o PCB
- Cables Dupont
- Fuente de alimentación 12V/2A

## 🔌 **Conexiones - ESP32**

```
ESP32          Componente
==============================
GPIO 4   -->   DHT22 (DATA)
GPIO 2   -->   PIR (OUT)
GPIO 34  -->   MQ-2 (A0)
GPIO 5   -->   Buzzer (+)
GPIO 6   -->   LED Verde (+)
GPIO 7   -->   LED Amarillo (+)
GPIO 8   -->   LED Rojo (+)
GPIO 9   -->   Relé Bomba (IN)
GPIO 10  -->   Relé Válvula (IN)
GPIO 21  -->   RFID (SDA/SS)
GPIO 22  -->   RFID (RST)
GPIO 23  -->   RFID (MOSI)
GPIO 19  -->   RFID (MISO)
GPIO 18  -->   RFID (SCK)

Alimentación:
5V       -->   DHT22, PIR, Buzzer, LEDs, RFID
3.3V     -->   MQ-2 (VCC)
GND      -->   Todos los GND
```

## ⚙️ **Configuración de Software**

### **Librerías Requeridas:**
```cpp
// Instalar desde el IDE de Arduino:
#include <WiFi.h>          // ESP32 Core
#include <HTTPClient.h>    // ESP32 Core  
#include <ArduinoJson.h>   // by Benoit Blanchon v6.21.3
#include <DHT.h>           // DHT sensor library v1.4.4
#include <SPI.h>           // Arduino Core
#include <MFRC522.h>       // MFRC522 library v1.4.10
```

### **Variables a Configurar:**
```cpp
// En el archivo .ino, cambiar estas variables:

// 1. Configuración WiFi
const char* ssid = "TU_WIFI_SSID";           
const char* password = "TU_WIFI_PASSWORD";    

// 2. IP del servidor Flask (cambiar por la IP de tu servidor)
const char* serverURL = "http://192.168.1.100:5000"; 

// 3. Tarjetas RFID autorizadas (obtener IDs reales)
String tarjetasAutorizadas[] = {
  "AB12CD34",    // Reemplazar con ID real de tarjeta
  "EF56GH78",    // Reemplazar con ID real de tarjeta
  "IJ90KL12"     // Reemplazar con ID real de tarjeta
};
```

## 📊 **Umbrales Configurables**

```cpp
// Temperatura
const float TEMP_MIN = 18.0;      // Mínima ideal
const float TEMP_MAX = 28.0;      // Máxima ideal  
const float TEMP_CRITICA = 35.0;  // Crítica alta

// Humedad
const float HUM_MIN = 40.0;       // Mínima ideal
const float HUM_MAX = 70.0;       // Máxima ideal
const float HUM_CRITICA_BAJA = 30.0;  // Crítica baja
const float HUM_CRITICA_ALTA = 80.0;  // Crítica alta

// Humo
const int HUMO_UMBRAL = 300;      // Detección
const int HUMO_CRITICO = 500;     // Crítico
```

## 🔍 **Cómo obtener IDs de tarjetas RFID**

1. **Cargar código de prueba:**
```cpp
#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN 22
#define SS_PIN 21

MFRC522 mfrc522(SS_PIN, RST_PIN);

void setup() {
  Serial.begin(115200);
  SPI.begin();
  mfrc522.PCD_Init();
  Serial.println("Acerca la tarjeta RFID...");
}

void loop() {
  if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
    String id = "";
    for (byte i = 0; i < mfrc522.uid.size; i++) {
      id += String(mfrc522.uid.uidByte[i], HEX);
    }
    id.toUpperCase();
    Serial.println("ID de tarjeta: " + id);
    delay(2000);
    mfrc522.PICC_HaltA();
  }
}
```

2. **Abrir Monitor Serie (115200 baud)**
3. **Acercar cada tarjeta al lector**
4. **Copiar los IDs mostrados**
5. **Reemplazar en el código principal**

## 📡 **Protocolo de Comunicación**

### **Datos enviados cada 30 segundos:**
```json
// POST /api/sensores/ambiente
{
  "temperatura": 25.6,
  "humedad": 65.2,
  "estado_bomba": "Encendida",
  "alerta": "Normal"
}
```

### **Alertas de seguridad (cuando ocurren):**
```json
// POST /api/sensores/seguridad  
{
  "tipo_evento": "Humo",
  "descripcion": "Nivel crítico detectado: 520",
  "nivel_alerta": "Crítico"
}
```

### **Registro de accesos (cuando se usa RFID):**
```json
// POST /api/sensores/acceso
{
  "id_tarjeta": "AB12CD34", 
  "persona": "Administrador",
  "estado_bomba": "Apagada",
  "temperatura": 24.1,
  "humedad": 58.3,
  "acceso_autorizado": true,
  "observacion": "Acceso normal"
}
```

## 🚨 **Sistema de Alertas**

### **Indicadores LED:**
- 🟢 **Verde**: Sistema normal
- 🟡 **Amarillo**: Advertencia (valores fuera de rango)  
- 🔴 **Rojo**: Alerta crítica

### **Buzzer:**
- **1 beep largo**: Acceso autorizado
- **5 beeps cortos**: Acceso denegado  
- **3 beeps intermitentes**: Alerta crítica

### **Control Automático:**
- **Bomba se enciende** cuando:
  - Temperatura > 28°C
  - Humedad < 40%
- **Bomba se apaga** cuando las condiciones se normalizan

## 🛠️ **Troubleshooting**

### **Problemas comunes:**

1. **No conecta a WiFi:**
   - Verificar SSID y password
   - Comprobar señal WiFi
   - Reiniciar ESP32

2. **Sensor DHT22 devuelve NaN:**
   - Verificar conexiones
   - Alimentación de 5V estable
   - Cambiar sensor si persiste

3. **RFID no lee tarjetas:**
   - Verificar conexiones SPI
   - Alimentación de 3.3V
   - Distancia < 3cm del lector

4. **No envía datos al servidor:**
   - Verificar IP del servidor
   - Comprobar que Flask esté ejecutándose
   - Revisar puerto 5000 abierto

### **Depuración:**
- Usar Monitor Serie a 115200 baud
- Todos los eventos se muestran en tiempo real
- LEDs indican estado visual del sistema