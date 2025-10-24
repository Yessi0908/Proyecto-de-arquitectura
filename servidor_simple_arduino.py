#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌿 SERVIDOR SIMPLE PARA ARDUINO ESP32 - GARANTIZADO
====================================================
Servidor Flask simple y funcional para Arduino ESP32
"""

from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
import pymysql
import os
from datetime import datetime

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

# HTML simple embebido
HTML_DASHBOARD = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌿 Invernadero Arduino ESP32</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }
        .card { 
            border-radius: 15px; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.1); 
            background: white;
            margin-bottom: 20px;
            padding: 20px;
            border: 1px solid #ddd;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        .row { display: flex; flex-wrap: wrap; margin: -10px; }
        .col-md-3, .col-md-6, .col-12 { padding: 10px; flex: 1; min-width: 250px; }
        .btn { 
            padding: 10px 15px; 
            margin: 5px; 
            border: none; 
            border-radius: 5px; 
            cursor: pointer; 
            font-weight: bold;
        }
        .btn-primary { background: #007bff; color: white; }
        .btn-success { background: #28a745; color: white; }
        .btn-info { background: #17a2b8; color: white; }
        .btn-warning { background: #ffc107; color: black; }
        .btn-danger { background: #dc3545; color: white; }
        .text-center { text-align: center; }
        .text-white { color: white; }
        .badge { padding: 5px 10px; border-radius: 12px; font-size: 12px; }
        .bg-secondary { background: #6c757d; }
        h1, h4, h6 { margin-top: 0; }
        code { background: #f8f9fa; padding: 10px; display: block; }
    </style>
</head>
<body>
    <div class="container py-4">
        <div class="row mb-4">
            <div class="col-12">
                <div class="card bg-white">
                    <div class="card-body text-center">
                        <h1 class="display-5 text-success">🌿 Sistema de Invernadero</h1>
                        <h6 class="text-muted">Monitoreo Arduino ESP32 - Datos Reales</h6>
                        <small class="text-muted">Servidor: 192.168.1.7:5000 | Configura Arduino con esta IP</small>
                    </div>
                </div>
            </div>
        </div>

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

        <div class="row mb-4">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header bg-primary text-white">
                        <h6 class="mb-0">📊 Últimos Registros</h6>
                    </div>
                    <div class="card-body">
                        <div id="registros">Cargando...</div>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header bg-info text-white">
                        <h6 class="mb-0">📈 Estadísticas</h6>
                    </div>
                    <div class="card-body">
                        <p><strong>Total registros:</strong> <span id="totalRegistros">0</span></p>
                        <p><strong>Registros hoy:</strong> <span id="registrosHoy">0</span></p>
                        <p><strong>Temp. promedio:</strong> <span id="promedioTemp">-- °C</span></p>
                        <p><strong>Humedad promedio:</strong> <span id="promedioHum">-- %</span></p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Controles y Acciones -->
        <div class="row mb-4">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header bg-warning text-dark">
                        <h6 class="mb-0">🎮 Controles del Sistema</h6>
                    </div>
                    <div class="card-body">
                        <button class="btn btn-primary me-2" onclick="simularDatos()">
                            🎲 Simular Datos
                        </button>
                        <button class="btn btn-info me-2" onclick="cargarDatos()">
                            🔄 Refrescar Datos
                        </button>
                        <button class="btn btn-success" onclick="descargarPDF()">
                            📄 Descargar PDF
                        </button>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header bg-danger text-white">
                        <h6 class="mb-0">⚠️ Control de Alertas</h6>
                    </div>
                    <div class="card-body">
                        <button class="btn btn-warning me-2" onclick="enviarAlerta('Medio')">
                            ⚡ Alerta Media
                        </button>
                        <button class="btn btn-danger" onclick="enviarAlerta('Alto')">
                            🚨 Alerta Alta
                        </button>
                        <div class="mt-2">
                            <small class="text-muted">Estado conexión Arduino: <span id="estadoArduino" class="badge bg-secondary">Desconocido</span></small>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header bg-success text-white">
                        <h6 class="mb-0">🔧 Configuración Arduino ESP32</h6>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-8">
                                <code style="background: #f8f9fa; padding: 10px; display: block;">
const char* ssid = "TU_RED_WIFI";<br>
const char* password = "TU_PASSWORD";<br>
const char* serverURL = "http://192.168.1.7:5000";
                                </code>
                                <small class="text-muted">Endpoint: POST /api/sensores/ambiente</small>
                            </div>
                            <div class="col-md-4">
                                <button class="btn btn-outline-primary btn-sm w-100 mb-2" onclick="copiarConfiguracion()">
                                    📋 Copiar Configuración
                                </button>
                                <button class="btn btn-outline-info btn-sm w-100" onclick="abrirDocumentacion()">
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
        async function cargarDatos() {
            try {
                const response = await fetch('/api/ambiente');
                const data = await response.json();
                
                if (data.ultimo_registro) {
                    const ultimo = data.ultimo_registro;
                    document.getElementById('temperatura').textContent = `${ultimo.temperatura}°C`;
                    document.getElementById('humedad').textContent = `${ultimo.humedad}%`;
                    document.getElementById('bomba').textContent = ultimo.estado_bomba;
                    document.getElementById('alerta').textContent = ultimo.alerta || 'Normal';
                    
                    const fecha = new Date(ultimo.fecha).toLocaleString();
                    document.getElementById('tempFecha').textContent = fecha;
                    document.getElementById('humFecha').textContent = fecha;
                    document.getElementById('bombaFecha').textContent = fecha;
                    document.getElementById('alertaFecha').textContent = fecha;
                }
                
                if (data.registros) {
                    let html = '';
                    data.registros.slice(-5).reverse().forEach(r => {
                        html += `<p><small>${new Date(r.fecha).toLocaleString()}</small><br>
                                 🌡️ ${r.temperatura}°C | 💧 ${r.humedad}% | 💡 ${r.estado_bomba}</p>`;
                    });
                    document.getElementById('registros').innerHTML = html || 'No hay registros';
                }
                
                document.getElementById('totalRegistros').textContent = data.total_registros || 0;
                document.getElementById('registrosHoy').textContent = data.registros_hoy || 0;
                document.getElementById('promedioTemp').textContent = `${data.promedio_temp || '--'}°C`;
                document.getElementById('promedioHum').textContent = `${data.promedio_hum || '--'}%`;
                
            } catch (error) {
                console.error('Error:', error);
                document.getElementById('registros').innerHTML = '❌ Error cargando datos';
            }
        }

        // Funciones de control
        async function simularDatos() {
            try {
                const response = await fetch('/api/simular_datos', { method: 'POST' });
                if (response.ok) {
                    document.getElementById('estadoArduino').textContent = 'Simulado';
                    document.getElementById('estadoArduino').className = 'badge bg-info';
                    setTimeout(cargarDatos, 1000);
                } else {
                    alert('Error simulando datos');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Error simulando datos');
            }
        }

        async function descargarPDF() {
            const btn = event.target;
            const originalText = btn.innerHTML;
            
            try {
                btn.innerHTML = '⏳ Generando PDF...';
                btn.disabled = true;
                
                console.log('🔄 Iniciando descarga de PDF...');
                const response = await fetch('/api/generar_pdf');
                
                console.log('📡 Respuesta:', response.status, response.statusText);
                
                if (response.ok) {
                    const contentType = response.headers.get('content-type');
                    console.log('📋 Content-Type:', contentType);
                    
                    if (contentType && contentType.includes('application/pdf')) {
                        const blob = await response.blob();
                        console.log('📁 Blob tamaño:', blob.size, 'bytes');
                        
                        const url = window.URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.href = url;
                        a.download = `reporte_invernadero_${new Date().toISOString().split('T')[0]}.pdf`;
                        document.body.appendChild(a);
                        a.click();
                        document.body.removeChild(a);
                        window.URL.revokeObjectURL(url);
                        
                        console.log('✅ PDF descargado exitosamente');
                        alert('✅ PDF descargado correctamente');
                    } else {
                        const errorText = await response.text();
                        console.error('❌ Respuesta no es PDF:', errorText);
                        alert('❌ Error: La respuesta no es un PDF válido');
                    }
                } else {
                    const errorText = await response.text();
                    console.error('❌ Error del servidor:', response.status, errorText);
                    alert(`❌ Error del servidor: ${response.status}`);
                }
            } catch (error) {
                console.error('❌ Error descargando PDF:', error);
                alert(`❌ Error: ${error.message}`);
            } finally {
                btn.innerHTML = originalText;
                btn.disabled = false;
            }
        }

        async function enviarAlerta(nivel) {
            try {
                const response = await fetch('/api/sensores/seguridad', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        tipo_evento: 'Prueba Manual',
                        descripcion: `Alerta de nivel ${nivel} generada manualmente`,
                        nivel_alerta: nivel
                    })
                });
                if (response.ok) {
                    alert(`Alerta ${nivel} enviada correctamente`);
                } else {
                    alert('Error enviando alerta');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Error enviando alerta');
            }
        }

        function copiarConfiguracion() {
            const config = `const char* ssid = "TU_RED_WIFI";
const char* password = "TU_PASSWORD";
const char* serverURL = "http://192.168.1.7:5000";`;
            navigator.clipboard.writeText(config).then(() => {
                alert('Configuración copiada al portapapeles');
            });
        }

        function abrirDocumentacion() {
            window.open('/docs', '_blank');
        }

        // Detectar estado Arduino basado en datos recientes
        function actualizarEstadoArduino(ultimoRegistro) {
            if (!ultimoRegistro) {
                document.getElementById('estadoArduino').textContent = 'Sin datos';
                document.getElementById('estadoArduino').className = 'badge bg-secondary';
                return;
            }
            
            const ahora = new Date();
            const ultimaFecha = new Date(ultimoRegistro.fecha);
            const minutosDiferencia = (ahora - ultimaFecha) / (1000 * 60);
            
            if (minutosDiferencia < 2) {
                document.getElementById('estadoArduino').textContent = 'Conectado';
                document.getElementById('estadoArduino').className = 'badge bg-success';
            } else if (minutosDiferencia < 5) {
                document.getElementById('estadoArduino').textContent = 'Intermitente';
                document.getElementById('estadoArduino').className = 'badge bg-warning';
            } else {
                document.getElementById('estadoArduino').textContent = 'Desconectado';
                document.getElementById('estadoArduino').className = 'badge bg-danger';
            }
        }

        // Modificar función cargarDatos para incluir estado Arduino
        const originalCargarDatos = cargarDatos;
        cargarDatos = async function() {
            await originalCargarDatos();
            // Obtener último registro para estado Arduino
            try {
                const response = await fetch('/api/ambiente');
                const data = await response.json();
                actualizarEstadoArduino(data.ultimo_registro);
            } catch (error) {
                console.error('Error actualizando estado Arduino:', error);
            }
        }

        // Cargar datos cada 10 segundos
        cargarDatos();
        setInterval(cargarDatos, 10000);
    </script>
</body>
</html>"""

@app.route('/')
def dashboard():
    """Dashboard principal"""
    return render_template_string(HTML_DASHBOARD)

@app.route('/api/health')
def health():
    """Estado del servidor"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'message': 'Servidor funcionando'
    })

@app.route('/api/ambiente')
def get_ambiente():
    """Obtener datos del ambiente"""
    conn = get_conn()
    if not conn:
        return jsonify({'error': 'Error de BD'}), 500
    
    try:
        with conn.cursor() as cur:
            # Último registro
            cur.execute("SELECT * FROM registros_ambiente ORDER BY fecha DESC LIMIT 1")
            ultimo_registro = cur.fetchone()
            
            # Todos los registros
            cur.execute("SELECT * FROM registros_ambiente ORDER BY fecha DESC LIMIT 50")
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
        print(f"❌ Error: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/sensores/ambiente', methods=['POST'])
def recibir_datos_arduino():
    """Recibir datos del Arduino ESP32"""
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
                cur.execute("""
                    INSERT INTO registros_ambiente (temperatura, humedad, estado_bomba, alerta) 
                    VALUES (%s, %s, %s, %s)
                """, (temperatura, humedad, estado_bomba, alerta))
            conn.commit()
            
            print(f"📡 Arduino: {temperatura}°C, {humedad}%, {estado_bomba}")
            
            return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()}), 201
        except Exception as e:
            print(f"❌ Error BD: {e}")
            return jsonify({'error': str(e)}), 500
        finally:
            conn.close()
            
    except Exception as e:
        print(f"❌ Error procesando: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/api/simular_datos', methods=['POST'])
def simular_datos():
    """Simular datos como si vinieran del Arduino"""
    import random
    try:
        # Generar datos simulados realistas
        temperatura = round(random.uniform(18.0, 32.0), 1)
        humedad = round(random.uniform(45.0, 85.0), 1)
        estado_bomba = "Encendida" if humedad < 60 else "Apagada"
        
        if temperatura > 30:
            alerta = "Alto"
        elif temperatura < 20 or humedad < 50:
            alerta = "Medio"
        else:
            alerta = "Normal"
        
        conn = get_conn()
        if not conn:
            return jsonify({'error': 'Error de BD'}), 500
        
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO registros_ambiente (temperatura, humedad, estado_bomba, alerta) 
                    VALUES (%s, %s, %s, %s)
                """, (temperatura, humedad, estado_bomba, alerta))
            conn.commit()
            
            print(f"🎲 Datos simulados: {temperatura}°C, {humedad}%, {estado_bomba}")
            
            return jsonify({
                'status': 'ok',
                'datos': {
                    'temperatura': temperatura,
                    'humedad': humedad,
                    'estado_bomba': estado_bomba,
                    'alerta': alerta
                }
            }), 201
        except Exception as e:
            print(f"❌ Error guardando simulación: {e}")
            return jsonify({'error': str(e)}), 500
        finally:
            conn.close()
            
    except Exception as e:
        print(f"❌ Error simulando datos: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/api/sensores/seguridad', methods=['POST'])
def recibir_alerta_seguridad():
    """Recibir alertas de seguridad"""
    try:
        data = request.get_json(force=True)
        tipo_evento = data.get('tipo_evento', 'Manual')
        descripcion = data.get('descripcion', '')
        nivel_alerta = data.get('nivel_alerta', 'Bajo')
        
        print(f"🚨 Alerta recibida: {tipo_evento} - {nivel_alerta}")
        print(f"   Descripción: {descripcion}")
        
        return jsonify({
            'status': 'ok',
            'message': 'Alerta registrada',
            'timestamp': datetime.now().isoformat()
        }), 201
        
    except Exception as e:
        print(f"❌ Error procesando alerta: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/api/generar_pdf')
def generar_pdf():
    """Generar reporte PDF mejorado pero simple"""
    print("🔄 Iniciando generación de PDF...")
    
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        from io import BytesIO
        
        # Crear PDF en memoria
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        
        # Título mejorado
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, 750, "🌿 REPORTE DEL SISTEMA DE INVERNADERO")
        p.setFont("Helvetica", 12)
        p.drawString(100, 730, f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Obtener datos de la BD
        conn = get_conn()
        if conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM registros_ambiente ORDER BY fecha DESC LIMIT 15")
                    registros = cur.fetchall()
                    
                    cur.execute("SELECT COUNT(*) as total FROM registros_ambiente")
                    total_result = cur.fetchone()
                    total = total_result['total'] if total_result else 0
                
                # Título
                p.drawString(100, 750, "REPORTE DEL SISTEMA DE INVERNADERO")
                p.drawString(100, 730, f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
                p.drawString(100, 710, f"Total de registros: {total}")
                
                # Encabezados
                y = 680
                p.drawString(100, y, "FECHA")
                p.drawString(200, y, "TEMP (°C)")
                p.drawString(280, y, "HUMEDAD (%)")
                p.drawString(360, y, "BOMBA")
                p.drawString(450, y, "ALERTA")
                
                # Datos
                y -= 20
                for registro in registros:
                    fecha_str = registro['fecha'].strftime('%Y-%m-%d %H:%M')
                    p.drawString(100, y, fecha_str)
                    p.drawString(200, y, str(registro['temperatura']))
                    p.drawString(280, y, str(registro['humedad']))
                    p.drawString(360, y, registro['estado_bomba'])
                    p.drawString(450, y, registro['alerta'] or 'Normal')
                    y -= 20
                    
                    if y < 100:  # Nueva página si es necesario
                        p.showPage()
                        y = 750
                
                conn.close()
                
            except Exception as e:
                p.drawString(100, 680, f"Error obteniendo datos: {e}")
        else:
            p.drawString(100, 680, "No se pudo conectar a la base de datos")
        
        p.save()
        buffer.seek(0)
        
        pdf_data = buffer.getvalue()
        print(f"✅ PDF generado exitosamente - Tamaño: {len(pdf_data)} bytes")
        
        from flask import Response
        return Response(
            pdf_data,
            mimetype='application/pdf',
            headers={
                'Content-Disposition': f'attachment; filename=reporte_invernadero_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf',
                'Content-Type': 'application/pdf',
                'Content-Length': str(len(pdf_data))
            }
        )
        
    except ImportError as ie:
        error_msg = 'ReportLab no está instalado. Use: pip install reportlab'
        print(f"❌ ImportError: {error_msg}")
        return jsonify({'error': error_msg}), 500
    except Exception as e:
        print(f"❌ Error generando PDF: {e}")
        return jsonify({'error': f'Error generando PDF: {str(e)}'}), 500

@app.route('/docs')
def documentacion():
    """Documentación del sistema"""
    docs_html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <title>Documentación - Sistema Invernadero</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light">
        <div class="container py-4">
            <h1 class="mb-4">📚 Documentación del Sistema</h1>
            
            <div class="card mb-4">
                <div class="card-header"><h3>🔧 Configuración Arduino ESP32</h3></div>
                <div class="card-body">
                    <pre><code>const char* ssid = "TU_RED_WIFI";
const char* password = "TU_PASSWORD";
const char* serverURL = "http://192.168.1.7:5000";</code></pre>
                </div>
            </div>
            
            <div class="card mb-4">
                <div class="card-header"><h3>📡 API Endpoints</h3></div>
                <div class="card-body">
                    <h5>POST /api/sensores/ambiente</h5>
                    <p>Recibe datos del Arduino ESP32:</p>
                    <pre><code>{
  "temperatura": 25.6,
  "humedad": 70.2,
  "estado_bomba": "Encendida",
  "alerta": "Normal"
}</code></pre>
                    
                    <h5>GET /api/ambiente</h5>
                    <p>Obtiene datos del sistema para dashboard</p>
                    
                    <h5>GET /api/generar_pdf</h5>
                    <p>Descarga reporte en PDF</p>
                </div>
            </div>
            
            <a href="/" class="btn btn-primary">← Volver al Dashboard</a>
        </div>
    </body>
    </html>
    """
    return docs_html

if __name__ == '__main__':
    print("🌿 SERVIDOR SIMPLE ARDUINO ESP32")
    print("=" * 40)
    print("🚀 Dashboard: http://192.168.1.7:5000")
    print("📡 Endpoint: POST /api/sensores/ambiente")
    print("⚙️ Configure Arduino con: serverURL = \"http://192.168.1.7:5000\";")
    print("=" * 40)
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False
    )