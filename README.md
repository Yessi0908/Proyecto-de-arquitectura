# Invernadero Automatizado IoT con Control de Acceso y Seguridad  
# Proyecto completo con Arduino, Flask, MySQL y Dashboard Web

# Descripción general
Este proyecto implementa un **invernadero automatizado y seguro**, con monitoreo ambiental, detección de movimiento, detección de humo y control de acceso RFID.  
Toda la información es enviada desde **Arduino/ESP32** hacia una **API Flask** y almacenada en una **base de datos MySQL** dentro de un contenedor **Docker**.  

Los datos se muestran en una **interfaz web** tipo dashboard, con íconos, tarjetas de estado y alertas visuales.

# Funcionalidades principales
- Monitoreo en tiempo real de **temperatura** y **humedad**.
- Activación automática de **bombas de agua** si los valores están fuera de rango.
- Alertas visuales cuando la temperatura o humedad alcanzan niveles críticos.

# Módulo de Seguridad
- **Detector de movimiento (PIR)**: registra actividad dentro del invernadero.
- **Sensor de humo (MQ-2)**: activa alertas y registra el evento en base de datos.
- Alertas visuales y sonoras (en el dashboard) cuando se detectan condiciones peligrosas.

### Módulo de Acceso RFID
- Registro de **entrada de personas mediante tarjeta RFID**.
- Guarda la **hora exacta de acceso**, el **nombre del usuario**, y el **estado del sistema** (bombas, temperatura, humedad) al momento del ingreso.
- Muestra accesos no autorizados con alerta roja.

### Interfaz Web Moderna
- Dashboard con **tarjetas de información** y **gráficos dinámicos**.
- **Filtros por fecha, tipo de evento o nivel de alerta.**
- **Exportación de registros en PDF.**
- Íconos para representar cada módulo (ambiente, seguridad, acceso).
- Alertas visuales en tiempo real (verde = normal, amarillo = advertencia, rojo = crítico).

## Tecnologías utilizadas
Lenguaje backend: Python 3 + Flask 
Base de datos: MySQL (contenedor Docker)
Frontend: HTML5, CSS3, JavaScript (Bootstrap o Tailwind opcional)
Comunicación IoT: WiFi (ESP32) o Serial (Arduino UNO)
Contenedores: Docker + Docker Compose
PDF reports:ReportLab 
Sensores: DHT11/DHT22, MQ-2, PIR, RFID 
Hardware: Arduino UNO o ESP32 

##  Estructura de la base de datos

```sql
CREATE TABLE registros_ambiente (
  id INT AUTO_INCREMENT PRIMARY KEY,
  fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
  temperatura FLOAT,
  humedad FLOAT,
  estado_bomba VARCHAR(15),
  alerta VARCHAR(50)
);

CREATE TABLE registros_seguridad (
  id INT AUTO_INCREMENT PRIMARY KEY,
  fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
  tipo_evento VARCHAR(50),
  descripcion TEXT,
  nivel_alerta VARCHAR(10)
);

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

## Configuración de Docker

Archivo `docker-compose.yml`:

```yaml
version: '3.8'
services:
  db:
    image: mysql:8.0
    container_name: invernadero_db
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: invernadero
    ports:
      - "3306:3306"
    volumes:
      - db_data:/var/lib/mysql

  backend:
    build: ./backend
    container_name: invernadero_backend
    ports:
      - "5000:5000"
    depends_on:
      - db
    environment:
      - DB_HOST=db
      - DB_USER=root
      - DB_PASSWORD=root
      - DB_NAME=invernadero

volumes:
  db_data:
```

##  Interfaz Web (HTML/CSS/JS)

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>🌿 Invernadero Automatizado</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    body { background-color: #d7f0d1; font-family: 'Poppins', sans-serif; }
    .card { border-radius: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
    .icon { font-size: 2rem; margin-right: 10px; }
    .alerta { font-weight: bold; }
  </style>
</head>
<body class="p-4">
  <div class="container">
    <h1 class="text-center mb-4">🌿 Panel de Control del Invernadero</h1>

    <div class="row g-4">
      <div class="col-md-4">
        <div class="card p-3 bg-light">
          <h5><span class="icon">🌡️</span>Ambiente</h5>
          <p>Temperatura: <strong id="temp">28°C</strong></p>
          <p>Humedad: <strong id="hum">52%</strong></p>
          <p>Estado bomba: <span class="alerta text-success">Apagada</span></p>
        </div>
      </div>

      <div class="col-md-4">
        <div class="card p-3 bg-light">
          <h5><span class="icon">🚨</span>Seguridad</h5>
          <p>Movimiento: <span id="mov">No detectado</span></p>
          <p>Humo: <span id="humo" class="text-success">Normal</span></p>
          <p>Alerta: <span id="alerta" class="text-success">🟢 Normal</span></p>
        </div>
      </div>

      <div class="col-md-4">
        <div class="card p-3 bg-light">
          <h5><span class="icon">🪪</span>Control de Acceso</h5>
          <p>Último acceso: <span id="horaAcceso">10:20 AM</span></p>
          <p>Usuario: <strong id="usuario">Juan Pérez</strong></p>
          <p>Acceso: <span class="text-success">Autorizado ✅</span></p>
        </div>
      </div>
    </div>

    <div class="card mt-4 p-4">
      <h5>📈 Registro de Temperatura y Humedad</h5>
      <canvas id="graficoAmbiente" height="100"></canvas>
    </div>

    <div class="card mt-4 p-4">
      <h5>🧾 Historial de eventos</h5>
      <table class="table table-hover">
        <thead class="table-success">
          <tr>
            <th>Fecha/Hora</th>
            <th>Evento</th>
            <th>Descripción</th>
            <th>Nivel</th>
          </tr>
        </thead>
        <tbody id="tablaEventos">
          <tr><td>2025-10-19 10:15</td><td>Movimiento</td><td>Zona norte</td><td>Medio</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <script>
    const ctx = document.getElementById('graficoAmbiente').getContext('2d');
    new Chart(ctx, {
      type: 'line',
      data: {
        labels: ['10:00','10:05','10:10','10:15','10:20'],
        datasets: [
          { label: 'Temperatura (°C)', data: [28,29,30,31,32], borderColor: 'red' },
          { label: 'Humedad (%)', data: [50,52,53,51,49], borderColor: 'blue' }
        ]
      }
    });
  </script>
</body>
</html>
```

## 📡 Comunicación Arduino–Servidor

```cpp
#include <WiFi.h>
#include <HTTPClient.h>

void enviarDatos(float temp, float hum, String estadoBomba) {
  HTTPClient http;
  http.begin("http://<IP_SERVIDOR>:5000/api/sensores/ambiente");
  http.addHeader("Content-Type", "application/json");
  String payload = "{"temperatura":" + String(temp) +
                   ","humedad":" + String(hum) +
                   ","estado_bomba":"" + estadoBomba + ""}";
  http.POST(payload);
  http.end();
}
```

