#!/usr/bin/env python3
"""
Servidor robusto para el sistema de invernadero
"""

import socket
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
import os
from datetime import datetime
import threading

# Datos simulados globales
datos_ambiente = [
    {'id': 1, 'fecha': '2025-10-23 19:30:00', 'temperatura': 25.5, 'humedad': 65.0, 'estado_bomba': 'Apagada', 'alerta': 'Normal'},
    {'id': 2, 'fecha': '2025-10-23 19:25:00', 'temperatura': 27.2, 'humedad': 58.0, 'estado_bomba': 'Apagada', 'alerta': 'Normal'},
    {'id': 3, 'fecha': '2025-10-23 19:20:00', 'temperatura': 23.8, 'humedad': 72.0, 'estado_bomba': 'Encendida', 'alerta': 'Medio'},
    {'id': 4, 'fecha': '2025-10-23 19:15:00', 'temperatura': 26.1, 'humedad': 62.0, 'estado_bomba': 'Apagada', 'alerta': 'Normal'},
    {'id': 5, 'fecha': '2025-10-23 19:10:00', 'temperatura': 24.7, 'humedad': 68.0, 'estado_bomba': 'Apagada', 'alerta': 'Normal'}
]

class RobustInvernaderoHandler(BaseHTTPRequestHandler):
    
    def log_message(self, format, *args):
        """Log personalizado"""
        print(f"🌐 [{datetime.now().strftime('%H:%M:%S')}] {format % args}")
    
    def send_cors_headers(self):
        """Enviar headers CORS"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    
    def send_json_response(self, data, status=200):
        """Enviar respuesta JSON"""
        try:
            self.send_response(status)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.send_cors_headers()
            self.end_headers()
            
            json_data = json.dumps(data, ensure_ascii=False, indent=2)
            self.wfile.write(json_data.encode('utf-8'))
            print(f"✅ Respuesta enviada: {len(json_data)} bytes")
        except Exception as e:
            print(f"❌ Error enviando respuesta: {e}")
    
    def send_html_response(self, html_content, status=200):
        """Enviar respuesta HTML"""
        try:
            self.send_response(status)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
            print(f"✅ HTML enviado: {len(html_content)} bytes")
        except Exception as e:
            print(f"❌ Error enviando HTML: {e}")

    def do_OPTIONS(self):
        """Manejar preflight CORS"""
        print("🔄 Manejo preflight OPTIONS")
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()

    def do_GET(self):
        """Manejar peticiones GET"""
        try:
            path = self.path.split('?')[0]
            print(f"📥 GET: {path}")
            
            if path == '/api/health':
                response = {
                    'status': 'ok',
                    'timestamp': datetime.now().isoformat(),
                    'message': 'Sistema funcionando correctamente',
                    'server': 'Servidor Robusto v2.0',
                    'port': 5000
                }
                self.send_json_response(response)
                
            elif path == '/api/ambiente':
                query_params = urllib.parse.parse_qs(self.path.split('?')[1] if '?' in self.path else '')
                limit = int(query_params.get('limit', [20])[0])
                response = datos_ambiente[:limit]
                self.send_json_response(response)
                
            elif path == '/api/estado/actual':
                ambiente = datos_ambiente[0] if datos_ambiente else None
                response = {
                    'ambiente': ambiente,
                    'seguridad': None,
                    'acceso': None,
                    'eventos': [
                        {
                            'fecha': r['fecha'],
                            'tipo': 'Ambiente',
                            'descripcion': f"T:{r['temperatura']}°C H:{r['humedad']}%",
                            'nivel': r['alerta']
                        } for r in datos_ambiente[:10]
                    ]
                }
                self.send_json_response(response)
                
            elif path == '/' or path == '/index.html':
                html_content = self.get_dashboard_html()
                self.send_html_response(html_content)
                
            elif path == '/test':
                html_content = self.get_test_html()
                self.send_html_response(html_content)
                
            else:
                self.send_json_response({'error': 'Endpoint no encontrado', 'path': path}, 404)
                
        except Exception as e:
            print(f"❌ Error en GET: {e}")
            self.send_json_response({'error': str(e)}, 500)

    def do_POST(self):
        """Manejar peticiones POST"""
        try:
            if self.path == '/api/simular_datos':
                import random
                nuevo = {
                    'id': len(datos_ambiente) + 1,
                    'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'temperatura': round(random.uniform(20.0, 30.0), 1),
                    'humedad': round(random.uniform(40.0, 80.0), 1),
                    'estado_bomba': random.choice(['Encendida', 'Apagada']),
                    'alerta': random.choice(['Normal', 'Normal', 'Medio'])
                }
                datos_ambiente.insert(0, nuevo)
                
                if len(datos_ambiente) > 50:
                    datos_ambiente[:] = datos_ambiente[:50]
                
                response = {
                    'message': 'Datos simulados correctamente',
                    'nuevo_registro': nuevo
                }
                self.send_json_response(response, 201)
            else:
                self.send_json_response({'error': 'Endpoint POST no encontrado'}, 404)
                
        except Exception as e:
            print(f"❌ Error en POST: {e}")
            self.send_json_response({'error': str(e)}, 500)

    def get_test_html(self):
        """Página de prueba simple"""
        return """
<!DOCTYPE html>
<html>
<head>
    <title>Test Invernadero</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f0f8ff; }
        .card { background: white; padding: 20px; border-radius: 10px; margin: 20px 0; }
        .success { color: green; }
        .error { color: red; }
        button { padding: 10px 20px; margin: 10px; background: #007bff; color: white; border: none; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>🌿 Test del Sistema de Invernadero</h1>
    
    <div class="card">
        <h3>Estado de Conexión</h3>
        <p id="status">Conectado ✅</p>
    </div>
    
    <div class="card">
        <h3>Datos Actuales</h3>
        <p>Temperatura: <span id="temp">--°C</span></p>
        <p>Humedad: <span id="hum">--%</span></p>
        <p>Estado Bomba: <span id="bomba">--</span></p>
    </div>
    
    <div class="card">
        <h3>Controles</h3>
        <button onclick="testAPI()">Probar API</button>
        <button onclick="simularDatos()">Simular Datos</button>
        <button onclick="irADashboard()">Ir a Dashboard</button>
    </div>
    
    <div class="card">
        <h3>Log</h3>
        <div id="log" style="height: 200px; overflow-y: scroll; background: #f8f8f8; padding: 10px;"></div>
    </div>

    <script>
        function log(msg) {
            const logDiv = document.getElementById('log');
            logDiv.innerHTML += new Date().toLocaleTimeString() + ': ' + msg + '\\n';
            logDiv.scrollTop = logDiv.scrollHeight;
        }

        async function testAPI() {
            try {
                log('Probando /api/health...');
                const response = await fetch('/api/health');
                const data = await response.json();
                log('✅ API funcionando: ' + data.message);
                
                log('Obteniendo estado actual...');
                const estadoRes = await fetch('/api/estado/actual');
                const estado = await estadoRes.json();
                
                if (estado.ambiente) {
                    document.getElementById('temp').textContent = estado.ambiente.temperatura + '°C';
                    document.getElementById('hum').textContent = estado.ambiente.humedad + '%';
                    document.getElementById('bomba').textContent = estado.ambiente.estado_bomba;
                    log('✅ Datos actualizados');
                } else {
                    log('⚠️ No hay datos de ambiente');
                }
            } catch (error) {
                log('❌ Error: ' + error.message);
            }
        }

        async function simularDatos() {
            try {
                log('Simulando nuevos datos...');
                const response = await fetch('/api/simular_datos', { method: 'POST' });
                const data = await response.json();
                log('✅ ' + data.message);
                setTimeout(testAPI, 1000);
            } catch (error) {
                log('❌ Error simulando: ' + error.message);
            }
        }
        
        function irADashboard() {
            window.location.href = '/';
        }

        // Test inicial
        window.onload = function() {
            log('Página cargada, probando conexión...');
            testAPI();
        };
    </script>
</body>
</html>
        """

    def get_dashboard_html(self):
        """Dashboard principal"""
        return """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌿 Invernadero Automatizado</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { background-color: #d7f0d1; }
        .card { border-radius: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
    </style>
</head>
<body class="p-4">
    <div class="container">
        <h1 class="text-center mb-4">🌿 Panel de Control del Invernadero</h1>
        
        <div class="alert alert-success text-center" id="status">
            ✅ Sistema conectado y funcionando
        </div>

        <div class="row g-4">
            <div class="col-md-4">
                <div class="card p-3">
                    <h5>🌡️ Ambiente</h5>
                    <p>Temperatura: <strong id="temp">--°C</strong></p>
                    <p>Humedad: <strong id="hum">--%</strong></p>
                    <p>Bomba: <strong id="bomba">--</strong></p>
                </div>
            </div>
            
            <div class="col-md-4">
                <div class="card p-3">
                    <h5>📊 Estadísticas</h5>
                    <p>Registros: <strong id="total">0</strong></p>
                    <p>Actualización: <strong id="update">--</strong></p>
                    <p>Servidor: <strong>Puerto 5000</strong></p>
                </div>
            </div>
            
            <div class="col-md-4">
                <div class="card p-3">
                    <h5>🔧 Controles</h5>
                    <button class="btn btn-primary w-100 mb-2" onclick="actualizar()">🔄 Actualizar</button>
                    <button class="btn btn-success w-100 mb-2" onclick="simular()">🎲 Simular</button>
                    <a href="/test" class="btn btn-info w-100">🧪 Página Test</a>
                </div>
            </div>
        </div>

        <div class="card mt-4 p-4">
            <h5>📈 Gráfico Temperatura y Humedad</h5>
            <canvas id="chart" height="100"></canvas>
        </div>

        <div class="card mt-4 p-4">
            <h5>📋 Historial Reciente</h5>
            <div class="table-responsive">
                <table class="table">
                    <thead>
                        <tr><th>Fecha</th><th>Temp</th><th>Hum</th><th>Bomba</th><th>Estado</th></tr>
                    </thead>
                    <tbody id="tabla"></tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
        let chart = null;

        async function actualizar() {
            try {
                document.getElementById('status').innerHTML = '🔄 Actualizando...';
                
                const response = await fetch('/api/estado/actual');
                const data = await response.json();
                
                if (data.ambiente) {
                    const amb = data.ambiente;
                    document.getElementById('temp').textContent = amb.temperatura + '°C';
                    document.getElementById('hum').textContent = amb.humedad + '%';
                    document.getElementById('bomba').textContent = amb.estado_bomba;
                    document.getElementById('update').textContent = new Date().toLocaleTimeString();
                }
                
                const ambienteRes = await fetch('/api/ambiente?limit=10');
                const ambiente = await ambienteRes.json();
                
                actualizarTabla(ambiente);
                actualizarGrafico(ambiente);
                
                document.getElementById('total').textContent = ambiente.length;
                document.getElementById('status').innerHTML = '✅ Sistema conectado y funcionando';
                
            } catch (error) {
                document.getElementById('status').innerHTML = '❌ Error: ' + error.message;
            }
        }

        async function simular() {
            try {
                await fetch('/api/simular_datos', { method: 'POST' });
                setTimeout(actualizar, 1000);
            } catch (error) {
                console.error('Error simulando:', error);
            }
        }

        function actualizarTabla(datos) {
            const tbody = document.getElementById('tabla');
            tbody.innerHTML = datos.map(r => `
                <tr>
                    <td>${new Date(r.fecha).toLocaleString()}</td>
                    <td><span class="badge bg-primary">${r.temperatura}°C</span></td>
                    <td><span class="badge bg-info">${r.humedad}%</span></td>
                    <td><span class="badge bg-${r.estado_bomba === 'Encendida' ? 'warning' : 'success'}">${r.estado_bomba}</span></td>
                    <td><span class="badge bg-${r.alerta === 'Normal' ? 'success' : 'warning'}">${r.alerta}</span></td>
                </tr>
            `).join('');
        }

        function actualizarGrafico(datos) {
            const ctx = document.getElementById('chart').getContext('2d');
            
            if (chart) chart.destroy();
            
            const labels = datos.slice().reverse().map(d => new Date(d.fecha).toLocaleTimeString());
            const tempData = datos.slice().reverse().map(d => d.temperatura);
            const humData = datos.slice().reverse().map(d => d.humedad);
            
            chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Temperatura (°C)',
                        data: tempData,
                        borderColor: 'rgb(255, 99, 132)',
                        tension: 0.4
                    }, {
                        label: 'Humedad (%)',
                        data: humData,
                        borderColor: 'rgb(54, 162, 235)',
                        tension: 0.4
                    }]
                },
                options: { responsive: true }
            });
        }

        window.onload = function() {
            actualizar();
            setInterval(actualizar, 30000);
        };
    </script>
</body>
</html>
        """

def encontrar_puerto_libre(start_port=5000):
    """Encuentra un puerto libre empezando desde start_port"""
    for port in range(start_port, start_port + 100):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(('127.0.0.1', port))
            sock.close()
            return port
        except OSError:
            continue
    return None

def main():
    # Encontrar puerto libre
    port = encontrar_puerto_libre(5000)
    if not port:
        print("❌ No se pudo encontrar un puerto libre")
        return
    
    server_address = ('127.0.0.1', port)
    
    try:
        httpd = HTTPServer(server_address, RobustInvernaderoHandler)
        
        print("🌿 SERVIDOR INVERNADERO INICIADO")
        print("=" * 50)
        print(f"🚀 URL: http://127.0.0.1:{port}")
        print(f"📊 Dashboard: http://127.0.0.1:{port}/")
        print(f"🧪 Test: http://127.0.0.1:{port}/test")
        print(f"📡 API: http://127.0.0.1:{port}/api/health")
        print("=" * 50)
        print("Presiona Ctrl+C para detener")
        
        httpd.serve_forever()
        
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido por el usuario")
    except Exception as e:
        print(f"❌ Error del servidor: {e}")
    finally:
        if 'httpd' in locals():
            httpd.server_close()

if __name__ == '__main__':
    main()