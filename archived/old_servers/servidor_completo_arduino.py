#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌿 SERVIDOR COMPLETO PARA ARDUINO ESP32 - CON BOTONES
======================================================
Servidor Flask completo con todas las funcionalidades
"""

from flask import Flask, jsonify, request, render_template_string, Response
from flask_cors import CORS
import pymysql
import os
from datetime import datetime
import random
from io import BytesIO

# Configuración
app = Flask(__name__)
CORS(app)

DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'root'
DB_NAME = 'invernadero'

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
        print(f"❌ Error BD: {e}")
        return None

# HTML completo con botones
HTML_DASHBOARD = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌿 Invernadero Arduino ESP32</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .card { border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
    </style>
</head>
<body>
    <div class="container py-4">
        <!-- Header -->
        <div class="row mb-4">
            <div class="col-12">
                <div class="card bg-white">
                    <div class="card-body text-center">
                        <h1 class="display-5 text-success">🌿 Sistema de Invernadero Arduino ESP32</h1>
                        <h6 class="text-muted">Monitoreo en Tiempo Real - Datos Reales</h6>
                        <small class="text-muted">Servidor: 192.168.1.7:5000 | Estado: <span id="estadoArduino" class="badge bg-secondary">Verificando...</span></small>
                    </div>
                </div>
            </div>
        </div>

        <!-- Métricas Principales -->
        <div class="row mb-4">
            <div class="col-md-3">
                <div class="card text-white" style="background: linear-gradient(45deg, #ff6b6b, #feca57);">
                    <div class="card-body text-center">
                        <h4 id="temperatura">-- °C</h4>
                        <p class="mb-0">Temperatura</p>
                        <small id="tempFecha">--</small>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-white" style="background: linear-gradient(45deg, #74b9ff, #0984e3);">
                    <div class="card-body text-center">
                        <h4 id="humedad">-- %</h4>
                        <p class="mb-0">Humedad</p>
                        <small id="humFecha">--</small>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-white" style="background: linear-gradient(45deg, #a29bfe, #6c5ce7);">
                    <div class="card-body text-center">
                        <h4 id="bomba">--</h4>
                        <p class="mb-0">Bomba</p>
                        <small id="bombaFecha">--</small>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-white" style="background: linear-gradient(45deg, #00b894, #00cec9);" id="alertaCard">
                    <div class="card-body text-center">
                        <h4 id="alerta">Normal</h4>
                        <p class="mb-0">Estado</p>
                        <small id="alertaFecha">--</small>
                    </div>
                </div>
            </div>
        </div>

        <!-- Controles -->
        <div class="row mb-4">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header bg-primary text-white">
                        <h6 class="mb-0">🎮 Controles del Sistema</h6>
                    </div>
                    <div class="card-body">
                        <button class="btn btn-success me-2 mb-2" onclick="descargarPDF()">
                            📄 Descargar PDF
                        </button>
                        <button class="btn btn-info me-2 mb-2" onclick="simularDatos()">
                            🎲 Simular Datos
                        </button>
                        <button class="btn btn-secondary mb-2" onclick="cargarDatos()">
                            🔄 Refrescar
                        </button>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header bg-warning text-dark">
                        <h6 class="mb-0">📊 Estadísticas</h6>
                    </div>
                    <div class="card-body">
                        <p><strong>Total registros:</strong> <span id="totalRegistros">0</span></p>
                        <p><strong>Registros hoy:</strong> <span id="registrosHoy">0</span></p>
                        <p><strong>Temp. promedio:</strong> <span id="promedioTemp">-- °C</span></p>
                        <p class="mb-0"><strong>Humedad promedio:</strong> <span id="promedioHum">-- %</span></p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Registros -->
        <div class="row mb-4">
            <div class="col-12">
                <div class="card">
                    <div class="card-header bg-info text-white">
                        <h6 class="mb-0">📈 Últimos Registros</h6>
                    </div>
                    <div class="card-body">
                        <div id="registros" class="table-responsive">Cargando...</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Configuración Arduino -->
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header bg-success text-white">
                        <h6 class="mb-0">🔧 Configuración Arduino ESP32</h6>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-8">
                                <code style="background: #f8f9fa; padding: 15px; display: block; font-size: 14px;">
const char* ssid = "TU_RED_WIFI";<br>
const char* password = "TU_PASSWORD";<br>
const char* serverURL = "http://192.168.1.7:5000";
                                </code>
                                <small class="text-muted mt-2 d-block">Endpoint: POST /api/sensores/ambiente</small>
                            </div>
                            <div class="col-md-4">
                                <button class="btn btn-outline-primary w-100 mb-2" onclick="copiarConfiguracion()">
                                    📋 Copiar Configuración
                                </button>
                                <button class="btn btn-outline-info w-100" onclick="window.open('/docs', '_blank')">
                                    📚 Ver Documentación
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Cargar datos del servidor
        async function cargarDatos() {
            try {
                const response = await fetch('/api/ambiente');
                const data = await response.json();
                
                if (data.ultimo_registro) {
                    const ultimo = data.ultimo_registro;
                    document.getElementById('temperatura').textContent = ultimo.temperatura + '°C';
                    document.getElementById('humedad').textContent = ultimo.humedad + '%';
                    document.getElementById('bomba').textContent = ultimo.estado_bomba;
                    document.getElementById('alerta').textContent = ultimo.alerta || 'Normal';
                    
                    const fecha = new Date(ultimo.fecha).toLocaleString();
                    document.getElementById('tempFecha').textContent = fecha;
                    document.getElementById('humFecha').textContent = fecha;
                    document.getElementById('bombaFecha').textContent = fecha;
                    document.getElementById('alertaFecha').textContent = fecha;
                    
                    // Estado Arduino
                    const ahora = new Date();
                    const ultimaFecha = new Date(ultimo.fecha);
                    const minutos = (ahora - ultimaFecha) / (1000 * 60);
                    
                    if (minutos < 2) {
                        document.getElementById('estadoArduino').textContent = 'Conectado';
                        document.getElementById('estadoArduino').className = 'badge bg-success';
                    } else if (minutos < 5) {
                        document.getElementById('estadoArduino').textContent = 'Intermitente';
                        document.getElementById('estadoArduino').className = 'badge bg-warning';
                    } else {
                        document.getElementById('estadoArduino').textContent = 'Desconectado';
                        document.getElementById('estadoArduino').className = 'badge bg-danger';
                    }
                }
                
                // Estadísticas
                document.getElementById('totalRegistros').textContent = data.total_registros || 0;
                document.getElementById('registrosHoy').textContent = data.registros_hoy || 0;
                document.getElementById('promedioTemp').textContent = (data.promedio_temp || '--') + '°C';
                document.getElementById('promedioHum').textContent = (data.promedio_hum || '--') + '%';
                
                // Últimos registros
                if (data.registros) {
                    let html = '<table class="table table-sm"><thead><tr><th>Fecha</th><th>Temp</th><th>Hum</th><th>Bomba</th><th>Alerta</th></tr></thead><tbody>';
                    data.registros.slice(-10).reverse().forEach(r => {
                        html += `<tr>
                            <td>${new Date(r.fecha).toLocaleString()}</td>
                            <td>${r.temperatura}°C</td>
                            <td>${r.humedad}%</td>
                            <td>${r.estado_bomba}</td>
                            <td><span class="badge ${r.alerta === 'Normal' ? 'bg-success' : r.alerta === 'Alto' ? 'bg-danger' : 'bg-warning'}">${r.alerta || 'Normal'}</span></td>
                        </tr>`;
                    });
                    html += '</tbody></table>';
                    document.getElementById('registros').innerHTML = html;
                } else {
                    document.getElementById('registros').innerHTML = '<p class="text-muted">No hay registros disponibles</p>';
                }
                
            } catch (error) {
                console.error('Error:', error);
                document.getElementById('estadoArduino').textContent = 'Error';
                document.getElementById('estadoArduino').className = 'badge bg-danger';
            }
        }

        // Simular datos
        async function simularDatos() {
            try {
                const response = await fetch('/api/simular_datos', { method: 'POST' });
                if (response.ok) {
                    setTimeout(cargarDatos, 1000);
                } else {
                    alert('Error simulando datos');
                }
            } catch (error) {
                alert('Error simulando datos');
            }
        }

        // Descargar PDF
        async function descargarPDF() {
            try {
                const response = await fetch('/api/generar_pdf');
                if (response.ok) {
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'reporte_invernadero_' + new Date().toISOString().split('T')[0] + '.pdf';
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                    window.URL.revokeObjectURL(url);
                } else {
                    alert('Error generando PDF');
                }
            } catch (error) {
                alert('Error descargando PDF');
            }
        }

        // Copiar configuración
        function copiarConfiguracion() {
            const config = 'const char* ssid = "TU_RED_WIFI";\\nconst char* password = "TU_PASSWORD";\\nconst char* serverURL = "http://192.168.1.7:5000";';
            navigator.clipboard.writeText(config).then(() => {
                alert('Configuración copiada al portapapeles');
            }).catch(() => {
                alert('No se pudo copiar la configuración');
            });
        }

        // Inicializar
        cargarDatos();
        setInterval(cargarDatos, 15000); // Actualizar cada 15 segundos
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    return render_template_string(HTML_DASHBOARD)

@app.route('/api/ambiente')
def get_ambiente():
    conn = get_conn()
    if not conn:
        return jsonify({'error': 'Error de BD'}), 500
    
    try:
        with conn.cursor() as cur:
            # Último registro
            cur.execute("SELECT * FROM registros_ambiente ORDER BY fecha DESC LIMIT 1")
            ultimo_registro = cur.fetchone()
            
            # Registros recientes
            cur.execute("SELECT * FROM registros_ambiente ORDER BY fecha DESC LIMIT 20")
            registros = cur.fetchall()
            
            # Estadísticas
            cur.execute("SELECT COUNT(*) as total FROM registros_ambiente")
            total_registros = cur.fetchone()['total']
            
            cur.execute("SELECT COUNT(*) as hoy FROM registros_ambiente WHERE DATE(fecha) = CURDATE()")
            registros_hoy = cur.fetchone()['hoy']
            
            cur.execute("SELECT AVG(temperatura) as temp, AVG(humedad) as hum FROM registros_ambiente WHERE fecha >= DATE_SUB(NOW(), INTERVAL 24 HOUR)")
            promedios = cur.fetchone()
            
            return jsonify({
                'ultimo_registro': ultimo_registro,
                'registros': registros,
                'total_registros': total_registros,
                'registros_hoy': registros_hoy,
                'promedio_temp': round(promedios['temp'] or 0, 1),
                'promedio_hum': round(promedios['hum'] or 0, 1)
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/sensores/ambiente', methods=['POST'])
def recibir_datos_arduino():
    try:
        data = request.get_json(force=True)
        temperatura = data.get('temperatura')
        humedad = data.get('humedad')
        estado_bomba = data.get('estado_bomba', 'Desconocido')
        alerta = data.get('alerta', 'Normal')
        
        conn = get_conn()
        if not conn:
            return jsonify({'error': 'Error de BD'}), 500
        
        try:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO registros_ambiente (temperatura, humedad, estado_bomba, alerta) VALUES (%s, %s, %s, %s)",
                           (temperatura, humedad, estado_bomba, alerta))
            conn.commit()
            print(f"📡 Arduino: {temperatura}°C, {humedad}%, {estado_bomba}")
            return jsonify({'status': 'ok'}), 201
        finally:
            conn.close()
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/simular_datos', methods=['POST'])
def simular_datos():
    try:
        # Datos simulados realistas
        temperatura = round(random.uniform(18.0, 32.0), 1)
        humedad = round(random.uniform(45.0, 85.0), 1)
        estado_bomba = "Encendida" if humedad < 60 else "Apagada"
        alerta = "Alto" if temperatura > 30 else "Normal"
        
        conn = get_conn()
        if not conn:
            return jsonify({'error': 'Error de BD'}), 500
        
        try:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO registros_ambiente (temperatura, humedad, estado_bomba, alerta) VALUES (%s, %s, %s, %s)",
                           (temperatura, humedad, estado_bomba, alerta))
            conn.commit()
            print(f"🎲 Simulado: {temperatura}°C, {humedad}%, {estado_bomba}")
            return jsonify({'status': 'ok'}), 201
        finally:
            conn.close()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generar_pdf')
def generar_pdf():
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        
        # Título
        p.drawString(100, 750, "REPORTE SISTEMA INVERNADERO ESP32")
        p.drawString(100, 730, f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        # Obtener datos
        conn = get_conn()
        if conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM registros_ambiente ORDER BY fecha DESC LIMIT 10")
                    registros = cur.fetchall()
                    
                    y = 680
                    p.drawString(100, y, "ULTIMOS REGISTROS:")
                    y -= 30
                    
                    for registro in registros:
                        fecha_str = registro['fecha'].strftime('%Y-%m-%d %H:%M')
                        texto = f"{fecha_str} - {registro['temperatura']}°C - {registro['humedad']}% - {registro['estado_bomba']}"
                        p.drawString(100, y, texto)
                        y -= 20
                        if y < 100:
                            break
                            
                conn.close()
            except Exception as e:
                p.drawString(100, 680, f"Error: {e}")
        
        p.save()
        buffer.seek(0)
        
        return Response(
            buffer.getvalue(),
            mimetype='application/pdf',
            headers={'Content-Disposition': f'attachment; filename=invernadero_{datetime.now().strftime("%Y%m%d")}.pdf'}
        )
        
    except ImportError:
        return jsonify({'error': 'Instale reportlab: pip install reportlab'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/docs')
def documentacion():
    return """
    <html><head><title>Documentación</title></head>
    <body style="font-family:Arial;margin:40px;">
    <h1>📚 Documentación Sistema Invernadero</h1>
    <h2>Configuración Arduino ESP32:</h2>
    <pre>const char* ssid = "TU_RED_WIFI";
const char* password = "TU_PASSWORD";
const char* serverURL = "http://192.168.1.7:5000";</pre>
    <h2>API Endpoints:</h2>
    <p><b>POST /api/sensores/ambiente</b> - Recibir datos del Arduino</p>
    <p><b>GET /api/ambiente</b> - Obtener datos del dashboard</p>
    <p><b>GET /api/generar_pdf</b> - Descargar reporte PDF</p>
    <br><a href="/">← Volver al Dashboard</a>
    </body></html>
    """

if __name__ == '__main__':
    print("🌿 SERVIDOR COMPLETO ARDUINO ESP32")
    print("=" * 40)
    print("🚀 Dashboard: http://192.168.1.7:5000")
    print("📄 Incluye: PDF, Simulación, Controles")
    print("📡 Endpoint: POST /api/sensores/ambiente")
    print("=" * 40)
    
    app.run(host='0.0.0.0', port=5000, debug=False)