#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <DHT.h>
#include <SPI.h>
#include <MFRC522.h>

// ===========================================
// CONFIGURACIÓN DE PINES
// ===========================================
#define DHT_PIN 4          // Pin del sensor DHT22
#define DHT_TYPE DHT22     // Tipo de sensor DHT

#define PIR_PIN 2          // Pin del sensor PIR
#define MQ2_PIN A0         // Pin analógico del sensor MQ-2
#define BUZZER_PIN 5       // Pin del buzzer
#define LED_VERDE 6        // LED verde (sistema normal)
#define LED_AMARILLO 7     // LED amarillo (advertencia)
#define LED_ROJO 8         // LED rojo (alerta crítica)

#define BOMBA_PIN 9        // Pin de control de la bomba de agua
#define VALVULA_PIN 10     // Pin de control de válvula adicional

// Pines del módulo RFID
#define RST_PIN 22
#define SS_PIN 21

// ===========================================
// CONFIGURACIÓN DE RED WIFI
// ===========================================
const char* ssid = "TU_WIFI_SSID";           // Cambiar por tu SSID
const char* password = "TU_WIFI_PASSWORD";    // Cambiar por tu password
const char* serverURL = "http://192.168.1.100:5000"; // IP del servidor Flask

// ===========================================
// INICIALIZACIÓN DE SENSORES
// ===========================================
DHT dht(DHT_PIN, DHT_TYPE);
MFRC522 mfrc522(SS_PIN, RST_PIN);

// ===========================================
// VARIABLES GLOBALES
// ===========================================
float temperatura = 0.0;
float humedad = 0.0;
bool bombaEncendida = false;
bool estadoPIR = false;
int nivelHumo = 0;
bool alertaHumo = false;

// Umbrales configurables
const float TEMP_MIN = 18.0;     // Temperatura mínima
const float TEMP_MAX = 28.0;     // Temperatura máxima
const float TEMP_CRITICA = 35.0; // Temperatura crítica

const float HUM_MIN = 40.0;      // Humedad mínima
const float HUM_MAX = 70.0;      // Humedad máxima
const float HUM_CRITICA_BAJA = 30.0;  // Humedad crítica baja
const float HUM_CRITICA_ALTA = 80.0;  // Humedad crítica alta

const int HUMO_UMBRAL = 300;     // Umbral de detección de humo
const int HUMO_CRITICO = 500;    // Nivel crítico de humo

// Tarjetas RFID autorizadas
String tarjetasAutorizadas[] = {
  "12345678",    // Tarjeta del administrador
  "87654321",    // Tarjeta del técnico
  "11223344"     // Tarjeta del supervisor
};
String nombresUsuarios[] = {
  "Administrador",
  "Técnico Agrícola", 
  "Supervisor"
};

// Timing para envío de datos
unsigned long ultimoEnvio = 0;
const unsigned long INTERVALO_ENVIO = 30000; // 30 segundos

// Timing para lecturas de sensores
unsigned long ultimaLectura = 0;
const unsigned long INTERVALO_LECTURA = 5000; // 5 segundos

void setup() {
  Serial.begin(115200);
  Serial.println("🌿 Iniciando Sistema de Invernadero Automatizado");
  
  // Inicializar pines
  pinMode(PIR_PIN, INPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(LED_VERDE, OUTPUT);
  pinMode(LED_AMARILLO, OUTPUT);
  pinMode(LED_ROJO, OUTPUT);
  pinMode(BOMBA_PIN, OUTPUT);
  pinMode(VALVULA_PIN, OUTPUT);
  
  // Estado inicial
  digitalWrite(BOMBA_PIN, LOW);
  digitalWrite(VALVULA_PIN, LOW);
  digitalWrite(LED_VERDE, HIGH);
  
  // Inicializar sensores
  dht.begin();
  SPI.begin();
  mfrc522.PCD_Init();
  
  // Conectar WiFi
  conectarWiFi();
  
  // Inicializar base de datos remota
  inicializarBaseDatos();
  
  Serial.println("✅ Sistema iniciado correctamente");
  Serial.println("📡 Monitoreando sensores...");
}

void loop() {
  unsigned long tiempoActual = millis();
  
  // Leer sensores cada 5 segundos
  if (tiempoActual - ultimaLectura >= INTERVALO_LECTURA) {
    leerSensores();
    procesarAlertas();
    controlarBomba();
    ultimaLectura = tiempoActual;
  }
  
  // Enviar datos cada 30 segundos
  if (tiempoActual - ultimoEnvio >= INTERVALO_ENVIO) {
    enviarDatos();
    ultimoEnvio = tiempoActual;
  }
  
  // Verificar acceso RFID
  verificarRFID();
  
  // Verificar conexión WiFi
  if (WiFi.status() != WL_CONNECTED) {
    conectarWiFi();
  }
  
  delay(1000);
}

// ===========================================
// FUNCIONES DE CONECTIVIDAD
// ===========================================
void conectarWiFi() {
  WiFi.begin(ssid, password);
  Serial.print("🔗 Conectando a WiFi");
  
  int intentos = 0;
  while (WiFi.status() != WL_CONNECTED && intentos < 30) {
    delay(1000);
    Serial.print(".");
    intentos++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println();
    Serial.println("✅ WiFi conectado!");
    Serial.print("📍 IP asignada: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println();
    Serial.println("❌ Error: No se pudo conectar a WiFi");
  }
}

void inicializarBaseDatos() {
  if (WiFi.status() != WL_CONNECTED) return;
  
  HTTPClient http;
  http.begin(String(serverURL) + "/api/init");
  http.addHeader("Content-Type", "application/json");
  
  int httpCode = http.POST("{}");
  if (httpCode == 201) {
    Serial.println("✅ Base de datos inicializada");
  } else {
    Serial.println("⚠️ Error inicializando base de datos: " + String(httpCode));
  }
  http.end();
}

// ===========================================
// FUNCIONES DE LECTURA DE SENSORES
// ===========================================
void leerSensores() {
  // Leer sensor DHT22
  temperatura = dht.readTemperature();
  humedad = dht.readHumidity();
  
  if (isnan(temperatura) || isnan(humedad)) {
    Serial.println("❌ Error leyendo sensor DHT22");
    return;
  }
  
  // Leer sensor PIR
  estadoPIR = digitalRead(PIR_PIN);
  
  // Leer sensor MQ-2
  nivelHumo = analogRead(MQ2_PIN);
  
  // Debug en Serial
  Serial.println("📊 Lecturas de sensores:");
  Serial.println("  🌡️ Temperatura: " + String(temperatura) + "°C");
  Serial.println("  💧 Humedad: " + String(humedad) + "%");
  Serial.println("  🚶 Movimiento: " + String(estadoPIR ? "Detectado" : "No detectado"));
  Serial.println("  💨 Nivel de humo: " + String(nivelHumo));
}

void procesarAlertas() {
  String nivelAlerta = "Normal";
  bool alertaCritica = false;
  
  // Verificar temperatura
  if (temperatura > TEMP_CRITICA) {
    nivelAlerta = "Crítico";
    alertaCritica = true;
    Serial.println("🚨 ALERTA CRÍTICA: Temperatura muy alta!");
  } else if (temperatura > TEMP_MAX || temperatura < TEMP_MIN) {
    nivelAlerta = "Alto";
    Serial.println("⚠️ ADVERTENCIA: Temperatura fuera de rango normal");
  }
  
  // Verificar humedad
  if (humedad < HUM_CRITICA_BAJA || humedad > HUM_CRITICA_ALTA) {
    nivelAlerta = "Crítico";
    alertaCritica = true;
    Serial.println("🚨 ALERTA CRÍTICA: Humedad en nivel crítico!");
  } else if (humedad < HUM_MIN || humedad > HUM_MAX) {
    if (nivelAlerta == "Normal") nivelAlerta = "Medio";
    Serial.println("⚠️ ADVERTENCIA: Humedad fuera de rango normal");
  }
  
  // Verificar humo
  if (nivelHumo > HUMO_CRITICO) {
    nivelAlerta = "Crítico";
    alertaCritica = true;
    alertaHumo = true;
    Serial.println("🚨 ALERTA CRÍTICA: Nivel de humo peligroso!");
    enviarAlertaSeguridad("Humo", "Nivel crítico detectado: " + String(nivelHumo), "Crítico");
  } else if (nivelHumo > HUMO_UMBRAL) {
    if (nivelAlerta == "Normal") nivelAlerta = "Medio";
    alertaHumo = true;
    Serial.println("⚠️ ADVERTENCIA: Humo detectado");
    enviarAlertaSeguridad("Humo", "Humo detectado: " + String(nivelHumo), "Medio");
  } else {
    alertaHumo = false;
  }
  
  // Verificar movimiento
  if (estadoPIR) {
    Serial.println("👤 Movimiento detectado en el invernadero");
    enviarAlertaSeguridad("Movimiento", "Actividad detectada en zona de cultivo", "Bajo");
  }
  
  // Controlar LEDs según alertas
  actualizarIndicadoresLED(nivelAlerta);
  
  // Activar buzzer si hay alerta crítica
  if (alertaCritica) {
    activarAlarma();
  }
}

void controlarBomba() {
  bool debeEncender = false;
  String razon = "";
  
  // Lógica de control automático
  if (temperatura > TEMP_MAX) {
    debeEncender = true;
    razon = "Temperatura alta: " + String(temperatura) + "°C";
  }
  
  if (humedad < HUM_MIN) {
    debeEncender = true;
    razon += (razon.length() > 0 ? " | " : "") + String("Humedad baja: ") + String(humedad) + "%";
  }
  
  // Control de la bomba
  if (debeEncender && !bombaEncendida) {
    digitalWrite(BOMBA_PIN, HIGH);
    digitalWrite(VALVULA_PIN, HIGH);
    bombaEncendida = true;
    Serial.println("💧 Bomba ENCENDIDA - " + razon);
  } else if (!debeEncender && bombaEncendida) {
    digitalWrite(BOMBA_PIN, LOW);
    digitalWrite(VALVULA_PIN, LOW);
    bombaEncendida = false;
    Serial.println("💧 Bomba APAGADA - Condiciones normalizadas");
  }
}

void actualizarIndicadoresLED(String nivel) {
  // Apagar todos los LEDs
  digitalWrite(LED_VERDE, LOW);
  digitalWrite(LED_AMARILLO, LOW);
  digitalWrite(LED_ROJO, LOW);
  
  if (nivel == "Crítico") {
    digitalWrite(LED_ROJO, HIGH);
  } else if (nivel == "Alto" || nivel == "Medio") {
    digitalWrite(LED_AMARILLO, HIGH);
  } else {
    digitalWrite(LED_VERDE, HIGH);
  }
}

void activarAlarma() {
  for (int i = 0; i < 3; i++) {
    digitalWrite(BUZZER_PIN, HIGH);
    delay(200);
    digitalWrite(BUZZER_PIN, LOW);
    delay(200);
  }
}

// ===========================================
// FUNCIONES DE COMUNICACIÓN CON SERVIDOR
// ===========================================
void enviarDatos() {
  if (WiFi.status() != WL_CONNECTED) return;
  
  HTTPClient http;
  http.begin(String(serverURL) + "/api/sensores/ambiente");
  http.addHeader("Content-Type", "application/json");
  
  // Crear JSON con datos
  DynamicJsonDocument doc(1024);
  doc["temperatura"] = temperatura;
  doc["humedad"] = humedad;
  doc["estado_bomba"] = bombaEncendida ? "Encendida" : "Apagada";
  
  String alerta = "Normal";
  if (temperatura > TEMP_CRITICA || humedad < HUM_CRITICA_BAJA || humedad > HUM_CRITICA_ALTA) {
    alerta = "Crítico";
  } else if (temperatura > TEMP_MAX || temperatura < TEMP_MIN || humedad < HUM_MIN || humedad > HUM_MAX) {
    alerta = "Alto";
  }
  doc["alerta"] = alerta;
  
  String jsonString;
  serializeJson(doc, jsonString);
  
  int httpCode = http.POST(jsonString);
  if (httpCode == 201) {
    Serial.println("📤 Datos enviados correctamente");
  } else {
    Serial.println("❌ Error enviando datos: " + String(httpCode));
  }
  http.end();
}

void enviarAlertaSeguridad(String tipo, String descripcion, String nivel) {
  if (WiFi.status() != WL_CONNECTED) return;
  
  HTTPClient http;
  http.begin(String(serverURL) + "/api/sensores/seguridad");
  http.addHeader("Content-Type", "application/json");
  
  DynamicJsonDocument doc(1024);
  doc["tipo_evento"] = tipo;
  doc["descripcion"] = descripcion;
  doc["nivel_alerta"] = nivel;
  
  String jsonString;
  serializeJson(doc, jsonString);
  
  int httpCode = http.POST(jsonString);
  if (httpCode == 201) {
    Serial.println("🚨 Alerta de seguridad enviada: " + tipo);
  } else {
    Serial.println("❌ Error enviando alerta: " + String(httpCode));
  }
  http.end();
}

// ===========================================
// FUNCIONES DE CONTROL DE ACCESO RFID
// ===========================================
void verificarRFID() {
  if (!mfrc522.PICC_IsNewCardPresent() || !mfrc522.PICC_ReadCardSerial()) {
    return;
  }
  
  // Leer ID de la tarjeta
  String idTarjeta = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    idTarjeta += String(mfrc522.uid.uidByte[i], HEX);
  }
  idTarjeta.toUpperCase();
  
  // Verificar si está autorizada
  bool autorizada = false;
  String nombreUsuario = "Desconocido";
  
  for (int i = 0; i < 3; i++) {
    if (idTarjeta == tarjetasAutorizadas[i]) {
      autorizada = true;
      nombreUsuario = nombresUsuarios[i];
      break;
    }
  }
  
  // Registrar acceso
  registrarAcceso(idTarjeta, nombreUsuario, autorizada);
  
  // Indicación visual y sonora
  if (autorizada) {
    Serial.println("✅ Acceso AUTORIZADO: " + nombreUsuario);
    digitalWrite(LED_VERDE, HIGH);
    digitalWrite(BUZZER_PIN, HIGH);
    delay(500);
    digitalWrite(BUZZER_PIN, LOW);
  } else {
    Serial.println("❌ Acceso DENEGADO: Tarjeta no autorizada");
    digitalWrite(LED_ROJO, HIGH);
    for (int i = 0; i < 5; i++) {
      digitalWrite(BUZZER_PIN, HIGH);
      delay(100);
      digitalWrite(BUZZER_PIN, LOW);
      delay(100);
    }
    // Enviar alerta de seguridad
    enviarAlertaSeguridad("Acceso", "Intento de acceso no autorizado: " + idTarjeta, "Alto");
  }
  
  delay(2000); // Evitar lecturas múltiples
  mfrc522.PICC_HaltA();
}

void registrarAcceso(String idTarjeta, String persona, bool autorizada) {
  if (WiFi.status() != WL_CONNECTED) return;
  
  HTTPClient http;
  http.begin(String(serverURL) + "/api/sensores/acceso");
  http.addHeader("Content-Type", "application/json");
  
  DynamicJsonDocument doc(1024);
  doc["id_tarjeta"] = idTarjeta;
  doc["persona"] = persona;
  doc["estado_bomba"] = bombaEncendida ? "Encendida" : "Apagada";
  doc["temperatura"] = temperatura;
  doc["humedad"] = humedad;
  doc["acceso_autorizado"] = autorizada;
  doc["observacion"] = autorizada ? "Acceso normal" : "Acceso denegado - tarjeta no autorizada";
  
  String jsonString;
  serializeJson(doc, jsonString);
  
  int httpCode = http.POST(jsonString);
  if (httpCode == 201) {
    Serial.println("📋 Acceso registrado correctamente");
  } else {
    Serial.println("❌ Error registrando acceso: " + String(httpCode));
  }
  http.end();
}