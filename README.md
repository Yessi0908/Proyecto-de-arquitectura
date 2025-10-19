# 🌿 Invernadero Automatizado IoT con Control de Acceso y Seguridad  
### 🧠 Proyecto completo con Arduino, Flask, MySQL y Dashboard Web

## 🏗️ Descripción general

Este proyecto implementa un **invernadero automatizado y seguro**, con monitoreo ambiental, detección de movimiento, detección de humo y control de acceso RFID.  
Toda la información es enviada desde **Arduino/ESP32** hacia una **API Flask** y almacenada en una **base de datos MySQL** dentro de un contenedor **Docker**.  

Los datos se muestran en una **interfaz web moderna** tipo dashboard, con íconos, tarjetas de estado y alertas visuales.

## 🚀 Funcionalidades principales

### 🌡️ Módulo Ambiental
- Monitoreo en tiempo real de **temperatura** y **humedad**.
- Activación automática de **bombas de agua** si los valores están fuera de rango.
- Alertas visuales cuando la temperatura o humedad alcanzan niveles críticos.

### 🚨 Módulo de Seguridad
- **Detector de movimiento (PIR)**: registra actividad dentro del invernadero.
- **Sensor de humo (MQ-2)**: activa alertas y registra el evento en base de datos.
- Alertas visuales y sonoras (en el dashboard) cuando se detectan condiciones peligrosas.

### 🪪 Módulo de Acceso RFID
- Registro de **entrada de personas mediante tarjeta RFID**.
- Guarda la **hora exacta de acceso**, el **nombre del usuario**, y el **estado del sistema** (bombas, temperatura, humedad) al momento del ingreso.
- Muestra accesos no autorizados con alerta roja.

### 🖥️ Interfaz Web Moderna
- Dashboard con **tarjetas de información** y **gráficos dinámicos**.
- **Filtros por fecha, tipo de evento o nivel de alerta.**
- **Exportación de registros en PDF.**
- Íconos para representar cada módulo (🌡️ ambiente, 🚨 seguridad, 🪪 acceso).
- Alertas visuales en tiempo real (verde = normal, amarillo = advertencia, rojo = crítico).

## ⚙️ Tecnologías utilizadas

| Componente | Tecnología |
|-------------|-------------|
| Lenguaje backend | 🐍 Python 3 + Flask |
| Base de datos | 🐬 MySQL (contenedor Docker) |
| Frontend | 🌐 HTML5, CSS3, JavaScript (Bootstrap o Tailwind opcional) |
| Comunicación IoT | WiFi (ESP32) o Serial (Arduino UNO) |
| Contenedores | 🐳 Docker + Docker Compose |
| PDF reports | 📄 ReportLab |
| Sensores | DHT11/DHT22, MQ-2, PIR, RFID |
| Hardware | Arduino UNO o ESP32 |

## 🗃️ Estructura de la base de datos

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

## 🐳 Configuración de Docker

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

## 🖼️ Interfaz Web (HTML/CSS/JS)

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

## ⚠️ Alertas dinámicas

| Tipo | Condición | Icono | Acción |
|------|------------|-------|--------|
| 🔥 Temperatura crítica | > 35°C | 🔴 | Mostrar alerta roja |
| 💨 Humo detectado | MQ-2 > umbral | 🔴 | Aviso de humo en pantalla |
| 🚶 Movimiento | PIR HIGH | 🟡 | Notificación visual |
| 🪪 Acceso denegado | RFID inválido | 🔴 | Mensaje de “Acceso restringido” |

## 🧾 Exportar reportes
- Filtros por fecha o tipo de evento.  
- Genera PDF con resumen de temperatura, humedad y alertas del día.

## 📋 Ejecución del sistema

```bash
git clone https://github.com/tuusuario/invernadero-automatizado.git
cd invernadero-automatizado
docker-compose up --build
```

Acceder desde el navegador: `http://localhost:5000`

## 🌐 Acceso desde otros dispositivos (LAN / Remoto)

Si quieres que la interfaz web sea accesible desde cualquier dispositivo de tu red local (por ejemplo, un móvil, tablet o otro ordenador), sigue estos pasos:

1. Averigua la IP local de la máquina que corre los contenedores (en Windows PowerShell):

```powershell
ipconfig | Select-String "IPv4"
```

2. Verifica que el puerto 5000 está escuchando y accesible desde la IP local (ejemplo si tu IP es 192.168.1.148):

```powershell
Test-NetConnection -ComputerName 192.168.1.148 -Port 5000
```

3. Si el puerto no es accesible, crea una regla de firewall para permitir conexiones entrantes en el puerto 5000 (ejecuta PowerShell como Administrador):

```powershell
New-NetFirewallRule -DisplayName "Invernadero HTTP 5000" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 5000 -Profile Private,Public
```

Para eliminar la regla más tarde:

```powershell
Remove-NetFirewallRule -DisplayName "Invernadero HTTP 5000"
```

4. Abre desde otro dispositivo en la misma red Wi‑Fi/ethernet la URL:

```
http://192.168.1.148:5000
```

Reemplaza `192.168.1.148` con la IP que obtuviste en el paso 1.

Nota: si tu PC está conectado a una red pública o corporativa, el router o políticas de red pueden bloquear conexiones entre dispositivos; prueba con una red doméstica.

## 🌍 Exponer la web públicamente (opciones)

Si quieres que la página sea accesible desde Internet (no solo LAN), tienes varias opciones. Ten en cuenta los riesgos de seguridad (exponer puertos/servicios públicamente requiere autenticación/HTTPS y configuración segura):

- Opción A — ngrok (rápido y seguro para pruebas):
  1. Regístrate y descarga ngrok desde https://ngrok.com
  2. Autentica tu cliente con tu token (solo la primera vez):

```powershell
ngrok authtoken <TU_AUTH_TOKEN>
```

  3. Abre un túnel HTTP al puerto 5000:

```powershell
ngrok http 5000
```

  ngrok te dará una URL pública (https) que redirige a tu `http://localhost:5000` — comparte esa URL para acceder desde cualquier lugar.

- Opción B — Port forwarding en tu router:
  - Configura una entrada NAT/Port Forwarding que redirija un puerto público (p. ej. 5000) hacia la IP local de tu equipo (192.168.1.148:5000).
  - En este caso usa también una regla de firewall y considera usar HTTPS mediante un proxy inverso (nginx) o un servicio de DNS dinámico.

- Opción C — Desplegar en un proveedor (Azure, AWS, DigitalOcean, Railway, Render):
  - Subir la app (backend) a un servicio que ofrezca HTTPS y dominio. Requiere cambios mínimos en configuración y una base de datos gestionada.

## 🔒 Recomendaciones de seguridad

- No expongas la base de datos MySQL directamente a Internet. Si usas ngrok o port forwarding, solo expón el puerto 5000 (backend), no 3306.
- Considera añadir autenticación básica o token para acceder a la interfaz y a la generación de PDF si la haces pública.
- Usa HTTPS en producción (ngrok ya lo ofrece para pruebas).


## 👨‍💻 Autoría
> Proyecto académico desarrollado como prototipo funcional de un **Invernadero Automatizado con sistema IoT, seguridad y control de acceso.**  
> **Autor:** *Tu Nombre*  
> **Licencia:** MIT  

🌱 *“Automatizar es sembrar futuro.”*
