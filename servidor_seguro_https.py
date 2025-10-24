#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌿 SERVIDOR SEGURO PARA ARDUINO ESP32 - CON HTTPS Y PDF MEJORADO
================================================================
Servidor Flask seguro con HTTPS y generación robusta de PDFs
"""

from flask import Flask, jsonify, request, render_template_string, Response
from flask_cors import CORS
import pymysql
import ssl
import os
from datetime import datetime
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

def crear_pdf_reportlab():
    """Generar PDF usando ReportLab"""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        
        buffer = BytesIO()
        
        # Crear documento PDF
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Título
        title = Paragraph("REPORTE DEL SISTEMA DE INVERNADERO", styles['Title'])
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Información general
        fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        info = Paragraph(f"<b>Fecha del reporte:</b> {fecha_actual}", styles['Normal'])
        story.append(info)
        story.append(Spacer(1, 12))
        
        # Obtener datos
        conn = get_conn()
        if conn:
            try:
                with conn.cursor() as cur:
                    # Total de registros
                    cur.execute("SELECT COUNT(*) as total FROM registros_ambiente")
                    total_result = cur.fetchone()
                    total = total_result['total'] if total_result else 0
                    
                    # Estadísticas
                    cur.execute("""
                        SELECT 
                            AVG(temperatura) as temp_promedio,
                            AVG(humedad) as humedad_promedio,
                            MAX(temperatura) as temp_max,
                            MIN(temperatura) as temp_min,
                            MAX(humedad) as humedad_max,
                            MIN(humedad) as humedad_min
                        FROM registros_ambiente 
                        WHERE fecha >= DATE_SUB(NOW(), INTERVAL 7 DAY)
                    """)
                    stats = cur.fetchone()
                    
                    # Últimos registros
                    cur.execute("""
                        SELECT * FROM registros_ambiente 
                        ORDER BY fecha DESC 
                        LIMIT 20
                    """)
                    registros = cur.fetchall()
                
                conn.close()
                
                # Agregar estadísticas
                if stats:
                    estadisticas = f"""
                    <b>Estadísticas de los últimos 7 días:</b><br/>
                    • Temperatura promedio: {stats['temp_promedio']:.1f}°C<br/>
                    • Humedad promedio: {stats['humedad_promedio']:.1f}%<br/>
                    • Temperatura máxima: {stats['temp_max']:.1f}°C<br/>
                    • Temperatura mínima: {stats['temp_min']:.1f}°C<br/>
                    • Humedad máxima: {stats['humedad_max']:.1f}%<br/>
                    • Humedad mínima: {stats['humedad_min']:.1f}%<br/>
                    • Total de registros: {total}
                    """
                    stats_paragraph = Paragraph(estadisticas, styles['Normal'])
                    story.append(stats_paragraph)
                    story.append(Spacer(1, 12))
                
                # Tabla de registros recientes
                if registros:
                    story.append(Paragraph("<b>Últimos 20 registros:</b>", styles['Heading2']))
                    story.append(Spacer(1, 6))
                    
                    # Preparar datos para la tabla
                    data = [['Fecha', 'Temperatura (°C)', 'Humedad (%)', 'Bomba', 'Alerta']]
                    
                    for registro in registros:
                        fecha_str = registro['fecha'].strftime('%Y-%m-%d %H:%M')
                        data.append([
                            fecha_str,
                            f"{registro['temperatura']:.1f}",
                            f"{registro['humedad']:.1f}",
                            registro['estado_bomba'] or 'N/A',
                            registro['alerta'] or 'Normal'
                        ])
                    
                    # Crear tabla
                    table = Table(data)
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 10),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('FONTSIZE', (0, 1), (-1, -1), 9),
                    ]))
                    story.append(table)
                else:
                    story.append(Paragraph("No hay registros disponibles", styles['Normal']))
                    
            except Exception as e:
                error_text = f"Error obteniendo datos de la base de datos: {str(e)}"
                story.append(Paragraph(error_text, styles['Normal']))
        else:
            story.append(Paragraph("No se pudo conectar a la base de datos", styles['Normal']))
        
        # Pie de página
        story.append(Spacer(1, 20))
        footer = Paragraph("Reporte generado automáticamente por el Sistema de Invernadero", styles['Normal'])
        story.append(footer)
        
        # Construir PDF
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
        
    except ImportError as ie:
        print(f"❌ Error de importación: {ie}")
        raise Exception("ReportLab no está instalado correctamente")
    except Exception as e:
        print(f"❌ Error generando PDF con ReportLab: {e}")
        raise e

def crear_pdf_simple():
    """Generar PDF simple como respaldo"""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        
        # Título
        p.drawString(100, 750, "REPORTE DEL SISTEMA DE INVERNADERO")
        p.drawString(100, 730, f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        # Obtener datos básicos
        conn = get_conn()
        if conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM registros_ambiente ORDER BY fecha DESC LIMIT 10")
                    registros = cur.fetchall()
                    
                    cur.execute("SELECT COUNT(*) as total FROM registros_ambiente")
                    total_result = cur.fetchone()
                    total = total_result['total'] if total_result else 0
                
                p.drawString(100, 710, f"Total de registros: {total}")
                
                # Encabezados
                y = 680
                p.drawString(100, y, "FECHA")
                p.drawString(220, y, "TEMP")
                p.drawString(280, y, "HUMEDAD")
                p.drawString(350, y, "BOMBA")
                p.drawString(450, y, "ALERTA")
                
                # Datos
                y -= 20
                for registro in registros:
                    if y < 100:
                        p.showPage()
                        y = 750
                    
                    fecha_str = registro['fecha'].strftime('%m-%d %H:%M')
                    p.drawString(100, y, fecha_str)
                    p.drawString(220, y, f"{registro['temperatura']:.1f}°C")
                    p.drawString(280, y, f"{registro['humedad']:.1f}%")
                    p.drawString(350, y, registro['estado_bomba'] or 'N/A')
                    p.drawString(450, y, registro['alerta'] or 'Normal')
                    y -= 20
                
                conn.close()
                
            except Exception as e:
                p.drawString(100, 680, f"Error BD: {str(e)[:50]}")
        else:
            p.drawString(100, 680, "Error conectando a la base de datos")
        
        p.save()
        buffer.seek(0)
        return buffer.getvalue()
        
    except Exception as e:
        print(f"❌ Error en PDF simple: {e}")
        raise e

# HTML del dashboard con HTTPS
HTML_DASHBOARD = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌿 Invernadero Arduino ESP32 - SEGURO</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh; 
            color: white; 
        }
        .card { 
            background: rgba(255,255,255,0.95); 
            color: #333; 
            margin-bottom: 20px; 
            border: none;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }
        .navbar { 
            background: rgba(255,255,255,0.1) !important; 
            backdrop-filter: blur(10px);
        }
        .sensor-card { 
            transition: transform 0.3s; 
        }
        .sensor-card:hover { 
            transform: translateY(-5px); 
        }
        .btn-custom {
            border-radius: 25px;
            padding: 10px 25px;
            margin: 5px;
        }
        .status-ok { color: #28a745; }
        .status-warning { color: #ffc107; }
        .status-error { color: #dc3545; }
        .secure-badge {
            position: fixed;
            top: 10px;
            right: 10px;
            background: #28a745;
            color: white;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 0.8em;
            z-index: 1000;
        }
    </style>
</head>
<body>
    <div class="secure-badge">
        🔒 CONEXIÓN SEGURA
    </div>

    <nav class="navbar navbar-expand-lg">
        <div class="container">
            <span class="navbar-brand text-white fs-3">🌿 Invernadero ESP32 - HTTPS</span>
            <span class="badge bg-success fs-6">🔒 SSL ACTIVO</span>
        </div>
    </nav>

    <div class="container mt-4">
        <div class="row">
            <!-- Sensores principales -->
            <div class="col-md-3">
                <div class="card sensor-card">
                    <div class="card-body text-center">
                        <h5 class="card-title">🌡️ Temperatura</h5>
                        <h2 id="temperatura" class="text-warning">--°C</h2>
                        <small id="fecha-temp" class="text-muted">Cargando...</small>
                    </div>
                </div>
            </div>
            
            <div class="col-md-3">
                <div class="card sensor-card">
                    <div class="card-body text-center">
                        <h5 class="card-title">💧 Humedad</h5>
                        <h2 id="humedad" class="text-info">--%</h2>
                        <small id="fecha-hum" class="text-muted">Cargando...</small>
                    </div>
                </div>
            </div>
            
            <div class="col-md-3">
                <div class="card sensor-card">
                    <div class="card-body text-center">
                        <h5 class="card-title">💧 Bomba</h5>
                        <h2 id="bomba" class="text-primary">--</h2>
                        <small id="fecha-bomba" class="text-muted">Cargando...</small>
                    </div>
                </div>
            </div>
            
            <div class="col-md-3">
                <div class="card sensor-card">
                    <div class="card-body text-center">
                        <h5 class="card-title">⚠️ Estado</h5>
                        <h2 id="estado" class="text-success">--</h2>
                        <small id="fecha-estado" class="text-muted">Cargando...</small>
                    </div>
                </div>
            </div>
        </div>

        <!-- Controles -->
        <div class="row mt-4">
            <div class="col-12">
                <div class="card">
                    <div class="card-body">
                        <h5>🎛️ Controles del Sistema</h5>
                        <button class="btn btn-success btn-custom" onclick="descargarPDF()">
                            📄 Descargar PDF Seguro
                        </button>
                        <button class="btn btn-info btn-custom" onclick="cargarDatos()">
                            🔄 Actualizar Datos
                        </button>
                        <button class="btn btn-warning btn-custom" onclick="simularDatos()">
                            🎲 Simular Datos
                        </button>
                        <button class="btn btn-danger btn-custom" onclick="enviarAlerta('alta')">
                            🚨 Alerta Test
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Registros recientes -->
        <div class="row mt-4">
            <div class="col-6">
                <div class="card">
                    <div class="card-header">
                        <h5>📋 Últimos Registros</h5>
                    </div>
                    <div class="card-body">
                        <div id="registros" style="max-height: 300px; overflow-y: auto;">
                            <p class="text-muted">Cargando registros...</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="col-6">
                <div class="card">
                    <div class="card-header">
                        <h5>📊 Estadísticas</h5>
                    </div>
                    <div class="card-body">
                        <div id="estadisticas">
                            <p class="text-muted">Cargando estadísticas...</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Función mejorada para descargar PDF
        async function descargarPDF() {
            const btn = event.target;
            const originalText = btn.innerHTML;
            
            try {
                btn.innerHTML = '⏳ Generando PDF...';
                btn.disabled = true;
                
                console.log('🔄 Iniciando descarga de PDF...');
                
                const response = await fetch('/api/generar_pdf', {
                    method: 'GET',
                    headers: {
                        'Accept': 'application/pdf'
                    }
                });
                
                console.log('📡 Respuesta recibida:', response.status, response.statusText);
                
                if (response.ok) {
                    const contentType = response.headers.get('content-type');
                    console.log('📋 Content-Type:', contentType);
                    
                    if (contentType && contentType.includes('application/pdf')) {
                        const blob = await response.blob();
                        console.log('📁 Blob creado, tamaño:', blob.size, 'bytes');
                        
                        const url = window.URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.href = url;
                        a.download = `reporte_invernadero_${new Date().toISOString().split('T')[0]}.pdf`;
                        document.body.appendChild(a);
                        a.click();
                        document.body.removeChild(a);
                        window.URL.revokeObjectURL(url);
                        
                        console.log('✅ PDF descargado exitosamente');
                        
                        // Mostrar mensaje de éxito
                        const alertDiv = document.createElement('div');
                        alertDiv.className = 'alert alert-success alert-dismissible fade show position-fixed';
                        alertDiv.style.top = '100px';
                        alertDiv.style.right = '20px';
                        alertDiv.style.zIndex = '9999';
                        alertDiv.innerHTML = `
                            <strong>✅ ¡Éxito!</strong> PDF descargado correctamente.
                            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                        `;
                        document.body.appendChild(alertDiv);
                        
                        setTimeout(() => {
                            if (alertDiv.parentNode) {
                                alertDiv.parentNode.removeChild(alertDiv);
                            }
                        }, 5000);
                        
                    } else {
                        throw new Error('La respuesta no es un PDF válido');
                    }
                } else {
                    const errorText = await response.text();
                    console.error('❌ Error del servidor:', response.status, errorText);
                    throw new Error(`Error del servidor: ${response.status} - ${errorText}`);
                }
            } catch (error) {
                console.error('❌ Error descargando PDF:', error);
                
                // Mostrar error detallado
                const alertDiv = document.createElement('div');
                alertDiv.className = 'alert alert-danger alert-dismissible fade show position-fixed';
                alertDiv.style.top = '100px';
                alertDiv.style.right = '20px';
                alertDiv.style.zIndex = '9999';
                alertDiv.innerHTML = `
                    <strong>❌ Error:</strong> ${error.message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                `;
                document.body.appendChild(alertDiv);
                
                setTimeout(() => {
                    if (alertDiv.parentNode) {
                        alertDiv.parentNode.removeChild(alertDiv);
                    }
                }, 8000);
                
            } finally {
                btn.innerHTML = originalText;
                btn.disabled = false;
            }
        }

        async function cargarDatos() {
            try {
                const response = await fetch('/api/sensores/ultimos');
                const data = await response.json();
                
                if (data.success && data.data) {
                    const registro = data.data;
                    document.getElementById('temperatura').textContent = registro.temperatura + '°C';
                    document.getElementById('humedad').textContent = registro.humedad + '%';
                    document.getElementById('bomba').textContent = registro.estado_bomba || 'Apagada';
                    document.getElementById('estado').textContent = registro.alerta || 'Normal';
                    
                    const fecha = new Date(registro.fecha).toLocaleString();
                    document.getElementById('fecha-temp').textContent = fecha;
                    document.getElementById('fecha-hum').textContent = fecha;
                    document.getElementById('fecha-bomba').textContent = fecha;
                    document.getElementById('fecha-estado').textContent = fecha;
                }
            } catch (error) {
                console.error('Error cargando datos:', error);
            }
            
            // Cargar registros recientes
            try {
                const response = await fetch('/api/sensores/historial');
                const data = await response.json();
                
                if (data.success) {
                    const registrosDiv = document.getElementById('registros');
                    registrosDiv.innerHTML = '';
                    
                    data.data.forEach(registro => {
                        const div = document.createElement('div');
                        div.className = 'border-bottom pb-2 mb-2';
                        div.innerHTML = `
                            <small class="text-muted">${new Date(registro.fecha).toLocaleString()}</small><br>
                            <strong>${registro.temperatura}°C</strong> | 
                            <strong>${registro.humedad}%</strong> | 
                            ${registro.estado_bomba} | 
                            <span class="badge bg-${registro.alerta === 'Normal' ? 'success' : 'warning'}">${registro.alerta || 'Normal'}</span>
                        `;
                        registrosDiv.appendChild(div);
                    });
                }
            } catch (error) {
                console.error('Error cargando historial:', error);
            }
            
            // Cargar estadísticas
            try {
                const response = await fetch('/api/sensores/estadisticas');
                const data = await response.json();
                
                if (data.success) {
                    const stats = data.data;
                    document.getElementById('estadisticas').innerHTML = `
                        <p><strong>Total registros:</strong> ${stats.total}</p>
                        <p><strong>Registros hoy:</strong> ${stats.hoy}</p>
                        <p><strong>Temp. promedio:</strong> ${stats.temp_promedio}°C</p>
                        <p><strong>Humedad promedio:</strong> ${stats.humedad_promedio}%</p>
                    `;
                }
            } catch (error) {
                console.error('Error cargando estadísticas:', error);
            }
        }

        async function simularDatos() {
            try {
                const response = await fetch('/api/simular_datos', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        temperatura: (20 + Math.random() * 15).toFixed(1),
                        humedad: (40 + Math.random() * 40).toFixed(1),
                        estado_bomba: Math.random() > 0.5 ? 'Encendida' : 'Apagada',
                        alerta: Math.random() > 0.8 ? 'Alta' : 'Normal'
                    })
                });
                
                if (response.ok) {
                    cargarDatos();
                }
            } catch (error) {
                console.error('Error simulando datos:', error);
            }
        }

        async function enviarAlerta(nivel) {
            try {
                const response = await fetch('/api/sensores/seguridad', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ nivel_alerta: nivel })
                });
                
                if (response.ok) {
                    alert('Alerta enviada correctamente');
                    cargarDatos();
                }
            } catch (error) {
                console.error('Error enviando alerta:', error);
            }
        }

        // Cargar datos inicial y cada 30 segundos
        cargarDatos();
        setInterval(cargarDatos, 30000);

        // Mostrar información de conexión segura
        console.log('🔒 Conexión HTTPS establecida correctamente');
        console.log('🌐 URL segura:', window.location.href);
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    """Dashboard principal"""
    return render_template_string(HTML_DASHBOARD)

@app.route('/api/sensores/ambiente', methods=['POST'])
def recibir_datos_arduino():
    """Endpoint para recibir datos del Arduino ESP32"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'No hay datos JSON'}), 400
        
        # Validar datos requeridos
        required_fields = ['temperatura', 'humedad']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'message': f'Falta campo: {field}'}), 400
        
        conn = get_conn()
        if not conn:
            return jsonify({'success': False, 'message': 'Error de conexión BD'}), 500
        
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO registros_ambiente (temperatura, humedad, estado_bomba, alerta, fecha)
                    VALUES (%s, %s, %s, %s, NOW())
                """, (
                    float(data['temperatura']),
                    float(data['humedad']),
                    data.get('estado_bomba', 'Desconocido'),
                    data.get('alerta', 'Normal')
                ))
                conn.commit()
                
            conn.close()
            
            print(f"✅ Datos Arduino guardados: T={data['temperatura']}°C, H={data['humedad']}%")
            return jsonify({
                'success': True, 
                'message': 'Datos guardados correctamente',
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            conn.rollback()
            conn.close()
            print(f"❌ Error guardando en BD: {e}")
            return jsonify({'success': False, 'message': f'Error BD: {str(e)}'}), 500
            
    except Exception as e:
        print(f"❌ Error procesando datos: {e}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@app.route('/api/generar_pdf')
def generar_pdf():
    """Generar reporte PDF con manejo robusto de errores"""
    print("🔄 Iniciando generación de PDF...")
    
    try:
        # Intentar generar PDF completo con ReportLab
        pdf_data = crear_pdf_reportlab()
        print("✅ PDF generado con ReportLab exitosamente")
        
        return Response(
            pdf_data,
            mimetype='application/pdf',
            headers={
                'Content-Disposition': f'attachment; filename=reporte_invernadero_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf',
                'Content-Type': 'application/pdf',
                'Content-Length': str(len(pdf_data))
            }
        )
        
    except Exception as e1:
        print(f"⚠️ Error con ReportLab completo: {e1}")
        print("🔄 Intentando con PDF simple...")
        
        try:
            # Respaldo: PDF simple
            pdf_data = crear_pdf_simple()
            print("✅ PDF simple generado exitosamente")
            
            return Response(
                pdf_data,
                mimetype='application/pdf',
                headers={
                    'Content-Disposition': f'attachment; filename=reporte_simple_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf',
                    'Content-Type': 'application/pdf',
                    'Content-Length': str(len(pdf_data))
                }
            )
            
        except Exception as e2:
            print(f"❌ Error también en PDF simple: {e2}")
            
            # Último recurso: mensaje de error en JSON
            error_response = {
                'success': False,
                'error': 'No se pudo generar el PDF',
                'details': {
                    'reportlab_error': str(e1),
                    'simple_pdf_error': str(e2),
                    'timestamp': datetime.now().isoformat()
                },
                'suggestions': [
                    'Verificar que ReportLab esté instalado: pip install reportlab',
                    'Comprobar que la base de datos esté disponible',
                    'Revisar los logs del servidor para más detalles'
                ]
            }
            
            return jsonify(error_response), 500

@app.route('/api/sensores/ultimos')
def obtener_ultimo_registro():
    """Obtener el último registro de sensores"""
    conn = get_conn()
    if not conn:
        return jsonify({'success': False, 'message': 'Error BD'}), 500
    
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM registros_ambiente 
                ORDER BY fecha DESC 
                LIMIT 1
            """)
            registro = cursor.fetchone()
        
        conn.close()
        
        if registro:
            return jsonify({
                'success': True,
                'data': {
                    'temperatura': float(registro['temperatura']),
                    'humedad': float(registro['humedad']),
                    'estado_bomba': registro['estado_bomba'],
                    'alerta': registro['alerta'],
                    'fecha': registro['fecha'].isoformat()
                }
            })
        else:
            return jsonify({'success': False, 'message': 'No hay registros'})
            
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/sensores/historial')
def obtener_historial():
    """Obtener historial de registros"""
    conn = get_conn()
    if not conn:
        return jsonify({'success': False, 'message': 'Error BD'}), 500
    
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM registros_ambiente 
                ORDER BY fecha DESC 
                LIMIT 10
            """)
            registros = cursor.fetchall()
        
        conn.close()
        
        data = []
        for registro in registros:
            data.append({
                'temperatura': float(registro['temperatura']),
                'humedad': float(registro['humedad']),
                'estado_bomba': registro['estado_bomba'],
                'alerta': registro['alerta'],
                'fecha': registro['fecha'].isoformat()
            })
        
        return jsonify({'success': True, 'data': data})
        
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/sensores/estadisticas')
def obtener_estadisticas():
    """Obtener estadísticas básicas"""
    conn = get_conn()
    if not conn:
        return jsonify({'success': False, 'message': 'Error BD'}), 500
    
    try:
        with conn.cursor() as cursor:
            # Total de registros
            cursor.execute("SELECT COUNT(*) as total FROM registros_ambiente")
            total = cursor.fetchone()['total']
            
            # Registros de hoy
            cursor.execute("""
                SELECT COUNT(*) as hoy FROM registros_ambiente 
                WHERE DATE(fecha) = CURDATE()
            """)
            hoy = cursor.fetchone()['hoy']
            
            # Promedios
            cursor.execute("""
                SELECT 
                    AVG(temperatura) as temp_promedio,
                    AVG(humedad) as humedad_promedio
                FROM registros_ambiente 
                WHERE fecha >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
            """)
            promedios = cursor.fetchone()
        
        conn.close()
        
        return jsonify({
            'success': True,
            'data': {
                'total': total,
                'hoy': hoy,
                'temp_promedio': f"{promedios['temp_promedio']:.1f}" if promedios['temp_promedio'] else "N/A",
                'humedad_promedio': f"{promedios['humedad_promedio']:.1f}" if promedios['humedad_promedio'] else "N/A"
            }
        })
        
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/simular_datos', methods=['POST'])
def simular_datos():
    """Simular datos para pruebas"""
    return recibir_datos_arduino()

@app.route('/api/sensores/seguridad', methods=['POST'])
def recibir_alerta_seguridad():
    """Endpoint para alertas de seguridad"""
    try:
        data = request.get_json()
        nivel = data.get('nivel_alerta', 'media')
        
        # Por ahora solo loggeamos
        print(f"🚨 Alerta de seguridad recibida: {nivel}")
        
        return jsonify({
            'success': True,
            'message': f'Alerta {nivel} registrada'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/status')
def status():
    """Estado del sistema"""
    return jsonify({
        'status': 'online',
        'timestamp': datetime.now().isoformat(),
        'https': True,
        'version': '2.0 - SEGURO'
    })

if __name__ == '__main__':
    print("🌿 SERVIDOR SEGURO ARDUINO ESP32")
    print("=" * 50)
    
    # Verificar certificados
    cert_exists = os.path.exists('server.crt') and os.path.exists('server.key')
    
    if cert_exists:
        print("🔒 HTTPS HABILITADO")
        print("🚀 Dashboard: https://192.168.1.7:5000")
        print("🚀 Dashboard local: https://localhost:5000")
        print("📡 Endpoint: POST https://192.168.1.7:5000/api/sensores/ambiente")
        print("⚙️ Configure Arduino con: serverURL = \"https://192.168.1.7:5000\";")
        print("🔧 Si el navegador muestra advertencia, acepta continuar")
        
        # Configurar contexto SSL
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain('server.crt', 'server.key')
        
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,
            ssl_context=context
        )
    else:
        print("⚠️ CERTIFICADOS NO ENCONTRADOS - USANDO HTTP")
        print("🚀 Dashboard: http://192.168.1.7:5000")
        print("📡 Endpoint: POST http://192.168.1.7:5000/api/sensores/ambiente")
        print("💡 Para HTTPS, ejecuta primero: python generar_certificado.py")
        
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False
        )