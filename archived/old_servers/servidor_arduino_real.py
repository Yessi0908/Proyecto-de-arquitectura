#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌿 SERVIDOR FLASK PARA ARDUINO ESP32 - DATOS REALES
=====================================================
Servidor Flask optimizado para recibir datos reales del Arduino ESP32
Sin simulación de datos - Listo para producción
"""

from flask import Flask, render_template_string, jsonify, request
from flask_cors import CORS
import pymysql
import os
from datetime import datetime, timedelta
import socket

# ===========================================
# CONFIGURACIÓN DEL SERVIDOR
# ===========================================
app = Flask(__name__)
CORS(app)

# Configuración de base de datos
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'root')
DB_NAME = os.environ.get('DB_NAME', 'invernadero')

def get_local_ip():
    """Obtener la IP local para configurar el Arduino"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

# ===========================================
# CONEXIÓN A BASE DE DATOS
# ===========================================
def get_conn():
    """Obtener conexión a MySQL"""
    try:
        return pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    except Exception as e:
        print(f"❌ Error conectando a BD: {e}")
        return None

# ===========================================
# PLANTILLA HTML EMBEBIDA
# ===========================================
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌿 Invernadero ESP32 - Monitoreo Real</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .card { border-radius: 20px; box-shadow: 0 8px 32px rgba(0,0,0,0.1); }
        .badge-temp { background: linear-gradient(45deg, #ff6b6b, #feca57); }
        .badge-hum { background: linear-gradient(45deg, #74b9ff, #0984e3); }
        .status-online { color: #00b894; }
        .status-offline { color: #e17055; }
        .status-waiting { color: #fdcb6e; }
    </style>
</head>
<body>
    <div class="container-fluid py-4">
        <!-- Header -->
        <div class="row mb-4">
            <div class="col-12">
                <div class="card bg-white">
                    <div class="card-body text-center">
                        <h1 class="display-4 text-success">🌿 Sistema de Invernadero</h1>
                        <h5 class="text-muted">Monitoreo en Tiempo Real - Arduino ESP32</h5>
                        <div id="connectionStatus" class="mt-2">
                            <span class="badge bg-warning fs-6">⏳ Esperando datos del Arduino...</span>
                        </div>
                        <small class="text-muted d-block mt-2">
                            IP del Servidor: <code>{{ local_ip }}:5000</code> | 
                            Configurar Arduino: <code>serverURL = "http://{{ local_ip }}:5000";</code>
                        </small>
                    </div>
                </div>
            </div>
        </div>

        <!-- Métricas Principales -->
        <div class="row mb-4">
            <div class="col-md-3">
                <div class="card text-white bg-gradient" style="background: linear-gradient(45deg, #ff6b6b, #feca57);">
                    <div class="card-body text-center">
                        <i class="fas fa-thermometer-half fa-2x mb-2"></i>
                        <h3 id="temperaturaActual">-- °C</h3>
                        <p class="mb-0">Temperatura</p>
                        <small id="tempTimestamp">--</small>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-white bg-gradient" style="background: linear-gradient(45deg, #74b9ff, #0984e3);">
                    <div class="card-body text-center">
                        <i class="fas fa-tint fa-2x mb-2"></i>
                        <h3 id="humedadActual">-- %</h3>
                        <p class="mb-0">Humedad</p>
                        <small id="humTimestamp">--</small>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-white bg-gradient" style="background: linear-gradient(45deg, #a29bfe, #6c5ce7);">
                    <div class="card-body text-center">
                        <i class="fas fa-water fa-2x mb-2"></i>
                        <h3 id="bombaEstado">--</h3>
                        <p class="mb-0">Bomba</p>
                        <small id="bombaTimestamp">--</small>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-white" id="alertaCard" style="background: linear-gradient(45deg, #00b894, #00cec9);">
                    <div class="card-body text-center">
                        <i class="fas fa-shield-alt fa-2x mb-2"></i>
                        <h3 id="nivelAlerta">Normal</h3>
                        <p class="mb-0">Estado</p>
                        <small id="alertaTimestamp">--</small>
                    </div>
                </div>
            </div>
        </div>

        <!-- Gráficos -->
        <div class="row mb-4">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header bg-primary text-white">
                        <h5 class="mb-0">📈 Temperatura (Últimas 24h)</h5>
                    </div>
                    <div class="card-body">
                        <canvas id="tempChart" height="300"></canvas>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header bg-info text-white">
                        <h5 class="mb-0">💧 Humedad (Últimas 24h)</h5>
                    </div>
                    <div class="card-body">
                        <canvas id="humChart" height="300"></canvas>
                    </div>
                </div>
            </div>
        </div>

        <!-- Estadísticas -->
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header bg-success text-white">
                        <h5 class="mb-0">📊 Estadísticas del Sistema</h5>
                    </div>
                    <div class="card-body">
                        <div class="row text-center">
                            <div class="col-md-3">
                                <h4 id="totalRegistros">0</h4>
                                <p class="text-muted">Registros Totales</p>
                            </div>
                            <div class="col-md-3">
                                <h4 id="registrosHoy">0</h4>
                                <p class="text-muted">Registros Hoy</p>
                            </div>
                            <div class="col-md-3">
                                <h4 id="promedioTemp">-- °C</h4>
                                <p class="text-muted">Temp. Promedio (24h)</p>
                            </div>
                            <div class="col-md-3">
                                <h4 id="promedioHum">-- %</h4>
                                <p class="text-muted">Humedad Promedio (24h)</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Scripts -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://kit.fontawesome.com/a076d05399.js"></script>
    <script>
        let tempChart, humChart;
        let ultimaActualizacion = null;
        let contadorConexion = 0;

        // Inicializar gráficos
        function initCharts() {
            const ctxTemp = document.getElementById('tempChart').getContext('2d');
            const ctxHum = document.getElementById('humChart').getContext('2d');

            tempChart = new Chart(ctxTemp, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Temperatura (°C)',
                        data: [],
                        borderColor: '#ff6b6b',
                        backgroundColor: 'rgba(255, 107, 107, 0.1)',
                        borderWidth: 3,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: true }
                    },
                    scales: {
                        y: { beginAtZero: false, title: { display: true, text: 'Temperatura (°C)' } },
                        x: { title: { display: true, text: 'Tiempo' } }
                    }
                }
            });

            humChart = new Chart(ctxHum, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Humedad (%)',
                        data: [],
                        borderColor: '#74b9ff',
                        backgroundColor: 'rgba(116, 185, 255, 0.1)',
                        borderWidth: 3,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: true }
                    },
                    scales: {
                        y: { beginAtZero: true, max: 100, title: { display: true, text: 'Humedad (%)' } },
                        x: { title: { display: true, text: 'Tiempo' } }
                    }
                }
            });
        }

        // Cargar datos
        async function cargarDatos() {
            try {
                const response = await fetch('/api/ambiente');
                const data = await response.json();
                
                if (data.registros && data.registros.length > 0) {
                    actualizarUI(data);
                    actualizarGraficos(data.registros);
                    actualizarEstadisticas(data);
                    actualizarEstadoConexion(true);
                } else {
                    actualizarEstadoConexion(false);
                }
            } catch (error) {
                console.error('Error cargando datos:', error);
                actualizarEstadoConexion(false);
            }
        }

        // Actualizar interfaz
        function actualizarUI(data) {
            if (data.ultimo_registro) {
                const ultimo = data.ultimo_registro;
                document.getElementById('temperaturaActual').textContent = `${ultimo.temperatura}°C`;
                document.getElementById('humedadActual').textContent = `${ultimo.humedad}%`;
                document.getElementById('bombaEstado').textContent = ultimo.estado_bomba;
                document.getElementById('nivelAlerta').textContent = ultimo.alerta || 'Normal';
                
                const fecha = new Date(ultimo.fecha).toLocaleString();
                document.getElementById('tempTimestamp').textContent = fecha;
                document.getElementById('humTimestamp').textContent = fecha;
                document.getElementById('bombaTimestamp').textContent = fecha;
                document.getElementById('alertaTimestamp').textContent = fecha;
                
                // Actualizar color según alerta
                const alertaCard = document.getElementById('alertaCard');
                const alerta = ultimo.alerta || 'Normal';
                if (alerta === 'Crítico') {
                    alertaCard.style.background = 'linear-gradient(45deg, #e17055, #d63031)';
                } else if (alerta === 'Alto') {
                    alertaCard.style.background = 'linear-gradient(45deg, #fdcb6e, #e17055)';
                } else {
                    alertaCard.style.background = 'linear-gradient(45deg, #00b894, #00cec9)';
                }
            }
        }

        // Actualizar gráficos
        function actualizarGraficos(registros) {
            const labels = registros.map(r => new Date(r.fecha).toLocaleTimeString());
            const temperaturas = registros.map(r => r.temperatura);
            const humedades = registros.map(r => r.humedad);

            tempChart.data.labels = labels;
            tempChart.data.datasets[0].data = temperaturas;
            tempChart.update();

            humChart.data.labels = labels;
            humChart.data.datasets[0].data = humedades;
            humChart.update();
        }

        // Actualizar estadísticas
        function actualizarEstadisticas(data) {
            document.getElementById('totalRegistros').textContent = data.total_registros || 0;
            document.getElementById('registrosHoy').textContent = data.registros_hoy || 0;
            document.getElementById('promedioTemp').textContent = `${data.promedio_temp || '--'}°C`;
            document.getElementById('promedioHum').textContent = `${data.promedio_hum || '--'}%`;
        }

        // Actualizar estado de conexión
        function actualizarEstadoConexion(conectado) {
            const statusDiv = document.getElementById('connectionStatus');
            const ahora = new Date();
            
            if (conectado) {
                ultimaActualizacion = ahora;
                contadorConexion = 0;
                statusDiv.innerHTML = '<span class="badge bg-success fs-6">✅ Arduino Conectado</span>';
            } else {
                contadorConexion++;
                if (contadorConexion > 4) {  // Más de 1 minuto sin datos
                    statusDiv.innerHTML = '<span class="badge bg-danger fs-6">❌ Arduino Desconectado</span>';
                } else {
                    statusDiv.innerHTML = '<span class="badge bg-warning fs-6">⏳ Esperando datos del Arduino...</span>';
                }
            }
        }

        // Inicializar
        document.addEventListener('DOMContentLoaded', function() {
            initCharts();
            cargarDatos();
            
            // Actualizar cada 15 segundos
            setInterval(cargarDatos, 15000);
        });
    </script>
</body>
</html>
"""

# ===========================================
# RUTAS DEL SERVIDOR
# ===========================================

@app.route('/')
def dashboard():
    """Dashboard principal del invernadero"""
    local_ip = get_local_ip()
    return render_template_string(DASHBOARD_HTML, local_ip=local_ip)

@app.route('/api/health')
def health_check():
    """Verificar estado del servidor"""
    return jsonify({
        'status': 'ok',
        'message': 'Servidor Flask activo',
        'timestamp': datetime.now().isoformat(),
        'database': 'connected' if get_conn() else 'disconnected',
        'local_ip': get_local_ip()
    })

@app.route('/api/ambiente')
def get_ambiente():
    """Obtener datos de ambiente (para dashboard)"""
    conn = get_conn()
    if not conn:
        return jsonify({'error': 'No se puede conectar a la base de datos'}), 500
    
    try:
        with conn.cursor() as cur:
            # Último registro
            cur.execute("""
                SELECT * FROM registros_ambiente 
                ORDER BY fecha DESC LIMIT 1
            """)
            ultimo_registro = cur.fetchone()
            
            # Registros de las últimas 24 horas
            cur.execute("""
                SELECT * FROM registros_ambiente 
                WHERE fecha >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
                ORDER BY fecha ASC
            """)
            registros_24h = cur.fetchall()
            
            # Estadísticas
            cur.execute("SELECT COUNT(*) as total FROM registros_ambiente")
            total_registros = cur.fetchone()['total']
            
            cur.execute("""
                SELECT COUNT(*) as hoy FROM registros_ambiente 
                WHERE DATE(fecha) = CURDATE()
            """)
            registros_hoy = cur.fetchone()['hoy']
            
            cur.execute("""
                SELECT AVG(temperatura) as temp, AVG(humedad) as hum 
                FROM registros_ambiente 
                WHERE fecha >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
            """)
            promedios = cur.fetchone()
            
            return jsonify({
                'ultimo_registro': ultimo_registro,
                'registros': registros_24h,
                'total_registros': total_registros,
                'registros_hoy': registros_hoy,
                'promedio_temp': round(promedios['temp'] or 0, 1),
                'promedio_hum': round(promedios['hum'] or 0, 1)
            })
    except Exception as e:
        print(f"❌ Error obteniendo ambiente: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/estado/actual')
def get_estado_actual():
    """Obtener estado actual del sistema (para compatibilidad)"""
    conn = get_conn()
    if not conn:
        return jsonify({'error': 'No se puede conectar a la base de datos'}), 500
    
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM registros_ambiente 
                ORDER BY fecha DESC LIMIT 1
            """)
            ultimo = cur.fetchone()
            
            if ultimo:
                return jsonify({
                    'temperatura': ultimo['temperatura'],
                    'humedad': ultimo['humedad'],
                    'estado_bomba': ultimo['estado_bomba'],
                    'alerta': ultimo['alerta'] or 'Normal',
                    'timestamp': ultimo['fecha'].isoformat()
                })
            else:
                return jsonify({
                    'temperatura': None,
                    'humedad': None,
                    'estado_bomba': 'Desconocido',
                    'alerta': 'Sin datos',
                    'timestamp': None
                })
    except Exception as e:
        print(f"❌ Error obteniendo estado actual: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

# ===========================================
# ENDPOINTS PARA ARDUINO ESP32
# ===========================================

@app.route('/api/sensores/ambiente', methods=['POST'])
def recibir_datos_ambiente():
    """Recibir datos del Arduino ESP32"""
    try:
        data = request.get_json(force=True)
        
        # Validar datos requeridos
        if not all(k in data for k in ['temperatura', 'humedad']):
            return jsonify({'error': 'Faltan datos requeridos'}), 400
        
        temperatura = float(data['temperatura'])
        humedad = float(data['humedad'])
        estado_bomba = data.get('estado_bomba', 'Desconocido')
        alerta = data.get('alerta', 'Normal')
        
        # Validar rangos de datos
        if not (-50 <= temperatura <= 100):
            return jsonify({'error': 'Temperatura fuera de rango'}), 400
        if not (0 <= humedad <= 100):
            return jsonify({'error': 'Humedad fuera de rango'}), 400
        
        conn = get_conn()
        if not conn:
            return jsonify({'error': 'Error de base de datos'}), 500
        
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO registros_ambiente (temperatura, humedad, estado_bomba, alerta) 
                    VALUES (%s, %s, %s, %s)
                """, (temperatura, humedad, estado_bomba, alerta))
            conn.commit()
            
            print(f"📡 Datos Arduino recibidos: {temperatura}°C, {humedad}%, {estado_bomba}, {alerta}")
            
            return jsonify({
                'status': 'ok',
                'message': 'Datos guardados correctamente',
                'timestamp': datetime.now().isoformat()
            }), 201
            
        except Exception as e:
            print(f"❌ Error guardando datos: {e}")
            return jsonify({'error': 'Error guardando datos'}), 500
        finally:
            conn.close()
            
    except Exception as e:
        print(f"❌ Error procesando datos del Arduino: {e}")
        return jsonify({'error': 'Error procesando datos'}), 400

@app.route('/api/sensores/seguridad', methods=['POST'])
def recibir_alerta_seguridad():
    """Recibir alertas de seguridad del Arduino"""
    try:
        data = request.get_json(force=True)
        
        tipo_evento = data.get('tipo_evento', 'Desconocido')
        descripcion = data.get('descripcion', '')
        nivel_alerta = data.get('nivel_alerta', 'Bajo')
        
        conn = get_conn()
        if not conn:
            return jsonify({'error': 'Error de base de datos'}), 500
        
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO registros_seguridad (tipo_evento, descripcion, nivel_alerta) 
                    VALUES (%s, %s, %s)
                """, (tipo_evento, descripcion, nivel_alerta))
            conn.commit()
            
            print(f"🚨 Alerta de seguridad: {tipo_evento} - {nivel_alerta}")
            
            return jsonify({
                'status': 'ok',
                'message': 'Alerta registrada',
                'timestamp': datetime.now().isoformat()
            }), 201
            
        except Exception as e:
            print(f"❌ Error guardando alerta: {e}")
            return jsonify({'error': 'Error guardando alerta'}), 500
        finally:
            conn.close()
            
    except Exception as e:
        print(f"❌ Error procesando alerta: {e}")
        return jsonify({'error': 'Error procesando alerta'}), 400

@app.route('/config')
def mostrar_configuracion():
    """Mostrar configuración del Arduino"""
    local_ip = get_local_ip()
    config_html = f"""
    <html>
    <head>
        <title>Configuración Arduino ESP32</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
            .config {{ background: white; padding: 20px; border-radius: 10px; max-width: 800px; }}
            code {{ background: #f8f8f8; padding: 10px; display: block; margin: 10px 0; border-radius: 5px; }}
        </style>
    </head>
    <body>
        <div class="config">
            <h1>🔧 Configuración del Arduino ESP32</h1>
            <p>Configura tu Arduino con estos parámetros:</p>
            
            <h3>🌐 Configuración de Red:</h3>
            <code>
const char* ssid = "TU_RED_WIFI";<br>
const char* password = "TU_PASSWORD_WIFI";<br>
const char* serverURL = "http://{local_ip}:5000";
            </code>
            
            <h3>📡 Endpoints disponibles:</h3>
            <ul>
                <li><strong>POST</strong> <code>/api/sensores/ambiente</code> - Enviar datos de temperatura y humedad</li>
                <li><strong>POST</strong> <code>/api/sensores/seguridad</code> - Enviar alertas de seguridad</li>
                <li><strong>GET</strong> <code>/api/health</code> - Verificar estado del servidor</li>
            </ul>
            
            <h3>📊 Formato JSON para datos de ambiente:</h3>
            <code>
{{"temperatura": 25.6, "humedad": 65.2, "estado_bomba": "Encendida", "alerta": "Normal"}}
            </code>
            
            <a href="/">← Volver al Dashboard</a>
        </div>
    </body>
    </html>
    """
    return config_html

# ===========================================
# INICIO DEL SERVIDOR
# ===========================================
if __name__ == '__main__':
    local_ip = get_local_ip()
    print("🌿 SERVIDOR FLASK PARA ARDUINO ESP32")
    print("=" * 50)
    print(f"🚀 Dashboard: http://{local_ip}:5000")
    print(f"🔧 Configuración: http://{local_ip}:5000/config")
    print(f"📡 API Health: http://{local_ip}:5000/api/health")
    print(f"📊 Endpoint Arduino: http://{local_ip}:5000/api/sensores/ambiente")
    print("=" * 50)
    print(f"📋 Configurar Arduino con: serverURL = \"http://{local_ip}:5000\";")
    print("⏳ Esperando datos del Arduino ESP32...")
    
    app.run(
        host='0.0.0.0',  # Permitir conexiones desde cualquier IP
        port=5000,
        debug=False,
        threaded=True
    )