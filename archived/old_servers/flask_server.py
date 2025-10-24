#!/usr/bin/env python3
"""
Servidor Flask simple y robusto para el invernadero
"""

from flask import Flask, jsonify, render_template_string
from flask_cors import CORS
import random
from datetime import datetime
import socket

app = Flask(__name__)
CORS(app)

# Datos simulados
datos_ambiente = [
    {'id': 1, 'fecha': '2025-10-23 19:30:00', 'temperatura': 25.5, 'humedad': 65.0, 'estado_bomba': 'Apagada', 'alerta': 'Normal'},
    {'id': 2, 'fecha': '2025-10-23 19:25:00', 'temperatura': 27.2, 'humedad': 58.0, 'estado_bomba': 'Apagada', 'alerta': 'Normal'},
    {'id': 3, 'fecha': '2025-10-23 19:20:00', 'temperatura': 23.8, 'humedad': 72.0, 'estado_bomba': 'Encendida', 'alerta': 'Medio'},
    {'id': 4, 'fecha': '2025-10-23 19:15:00', 'temperatura': 26.1, 'humedad': 62.0, 'estado_bomba': 'Apagada', 'alerta': 'Normal'},
    {'id': 5, 'fecha': '2025-10-23 19:10:00', 'temperatura': 24.7, 'humedad': 68.0, 'estado_bomba': 'Apagada', 'alerta': 'Normal'}
]

@app.route('/api/health')
def api_health():
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'message': 'Sistema de invernadero funcionando correctamente',
        'server': 'Flask Simple v1.0'
    })

@app.route('/api/ambiente')
def api_ambiente():
    return jsonify(datos_ambiente)

@app.route('/api/estado/actual')
def api_estado_actual():
    ambiente = datos_ambiente[0] if datos_ambiente else None
    return jsonify({
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
    })

@app.route('/api/simular_datos', methods=['POST'])
def api_simular_datos():
    global datos_ambiente
    
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
        datos_ambiente = datos_ambiente[:50]
    
    return jsonify({
        'message': 'Datos simulados correctamente',
        'nuevo_registro': nuevo
    }), 201

@app.route('/')
def dashboard():
    return render_template_string(DASHBOARD_HTML)

@app.route('/test')
def test_page():
    return render_template_string(TEST_HTML)

# Template del dashboard
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌿 Invernadero Automatizado</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { background: linear-gradient(135deg, #d7f0d1, #a8e6cf); }
        .card { border-radius: 15px; box-shadow: 0 6px 15px rgba(0,0,0,0.1); border: none; }
        .card-header { background: rgba(255,255,255,0.9); border-radius: 15px 15px 0 0 !important; }
        .navbar { background: rgba(255,255,255,0.95); backdrop-filter: blur(10px); }
        .status-ok { color: #28a745; }
        .status-warning { color: #fd7e14; }
        .status-danger { color: #dc3545; }
        .pulse { animation: pulse 2s infinite; }
        @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light mb-4">
        <div class="container">
            <span class="navbar-brand mb-0 h1">🌿 Sistema de Invernadero IoT</span>
            <div class="navbar-nav ms-auto">
                <span class="nav-link pulse" id="connectionStatus">🟢 Conectado</span>
            </div>
        </div>
    </nav>

    <div class="container">
        <div class="row g-4 mb-4">
            <div class="col-md-3">
                <div class="card text-center">
                    <div class="card-body">
                        <div style="font-size: 3rem;">🌡️</div>
                        <h5>Temperatura</h5>
                        <h3 id="temp" class="status-ok">--°C</h3>
                        <small class="text-muted">Actual</small>
                    </div>
                </div>
            </div>
            
            <div class="col-md-3">
                <div class="card text-center">
                    <div class="card-body">
                        <div style="font-size: 3rem;">💧</div>
                        <h5>Humedad</h5>
                        <h3 id="hum" class="status-ok">--%</h3>
                        <small class="text-muted">Relativa</small>
                    </div>
                </div>
            </div>
            
            <div class="col-md-3">
                <div class="card text-center">
                    <div class="card-body">
                        <div style="font-size: 3rem;">⚡</div>
                        <h5>Bomba</h5>
                        <h3 id="bomba" class="status-ok">--</h3>
                        <small class="text-muted">Estado</small>
                    </div>
                </div>
            </div>
            
            <div class="col-md-3">
                <div class="card text-center">
                    <div class="card-body">
                        <div style="font-size: 3rem;">📊</div>
                        <h5>Registros</h5>
                        <h3 id="total" class="status-ok">0</h3>
                        <small class="text-muted">Total</small>
                    </div>
                </div>
            </div>
        </div>

        <div class="row g-4 mb-4">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header">
                        <h5 class="mb-0">📈 Monitoreo en Tiempo Real</h5>
                    </div>
                    <div class="card-body">
                        <canvas id="chart" height="100"></canvas>
                    </div>
                </div>
            </div>
            
            <div class="col-md-4">
                <div class="card">
                    <div class="card-header">
                        <h5 class="mb-0">🎛️ Panel de Control</h5>
                    </div>
                    <div class="card-body">
                        <button class="btn btn-primary w-100 mb-3" onclick="actualizar()">
                            🔄 Actualizar Datos
                        </button>
                        <button class="btn btn-success w-100 mb-3" onclick="simular()">
                            🎲 Simular Datos
                        </button>
                        <a href="/test" class="btn btn-info w-100 mb-3">
                            🧪 Página de Pruebas
                        </a>
                        <div class="mt-3">
                            <small class="text-muted">
                                Última actualización: <br>
                                <span id="lastUpdate">--:--:--</span>
                            </small>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="card">
            <div class="card-header">
                <h5 class="mb-0">📋 Historial de Registros</h5>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-hover">
                        <thead class="table-dark">
                            <tr>
                                <th>📅 Fecha y Hora</th>
                                <th>🌡️ Temperatura</th>
                                <th>💧 Humedad</th>
                                <th>⚡ Bomba</th>
                                <th>🚨 Estado</th>
                            </tr>
                        </thead>
                        <tbody id="tabla">
                            <tr><td colspan="5" class="text-center">Cargando datos...</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <script>
        let chart = null;
        let isUpdating = false;

        function updateConnectionStatus(connected) {
            const status = document.getElementById('connectionStatus');
            if (connected) {
                status.innerHTML = '🟢 Conectado';
                status.className = 'nav-link pulse';
            } else {
                status.innerHTML = '🔴 Desconectado';
                status.className = 'nav-link';
            }
        }

        async function actualizar() {
            if (isUpdating) return;
            isUpdating = true;
            
            try {
                updateConnectionStatus(true);
                
                // Obtener estado actual
                const estadoRes = await fetch('/api/estado/actual');
                const estado = await estadoRes.json();
                
                if (estado.ambiente) {
                    const amb = estado.ambiente;
                    document.getElementById('temp').textContent = amb.temperatura + '°C';
                    document.getElementById('hum').textContent = amb.humedad + '%';
                    document.getElementById('bomba').textContent = amb.estado_bomba;
                    
                    // Colores según valores
                    const tempEl = document.getElementById('temp');
                    tempEl.className = amb.temperatura > 28 ? 'status-danger' : amb.temperatura < 20 ? 'status-warning' : 'status-ok';
                    
                    const humEl = document.getElementById('hum');
                    humEl.className = amb.humedad > 80 ? 'status-warning' : amb.humedad < 40 ? 'status-warning' : 'status-ok';
                    
                    const bombaEl = document.getElementById('bomba');
                    bombaEl.className = amb.estado_bomba === 'Encendida' ? 'status-warning' : 'status-ok';
                }
                
                // Obtener datos de ambiente
                const ambienteRes = await fetch('/api/ambiente');
                const ambiente = await ambienteRes.json();
                
                document.getElementById('total').textContent = ambiente.length;
                document.getElementById('lastUpdate').textContent = new Date().toLocaleTimeString();
                
                actualizarTabla(ambiente);
                actualizarGrafico(ambiente);
                
            } catch (error) {
                console.error('Error:', error);
                updateConnectionStatus(false);
            } finally {
                isUpdating = false;
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
            if (datos.length === 0) {
                tbody.innerHTML = '<tr><td colspan="5" class="text-center">No hay datos disponibles</td></tr>';
                return;
            }
            
            tbody.innerHTML = datos.slice(0, 10).map(r => `
                <tr>
                    <td>${new Date(r.fecha).toLocaleString()}</td>
                    <td><span class="badge bg-${r.temperatura > 28 ? 'danger' : r.temperatura < 20 ? 'warning' : 'success'}">${r.temperatura}°C</span></td>
                    <td><span class="badge bg-${r.humedad > 80 ? 'warning' : r.humedad < 40 ? 'warning' : 'primary'}">${r.humedad}%</span></td>
                    <td><span class="badge bg-${r.estado_bomba === 'Encendida' ? 'warning' : 'success'}">${r.estado_bomba}</span></td>
                    <td><span class="badge bg-${r.alerta === 'Normal' ? 'success' : r.alerta === 'Medio' ? 'warning' : 'danger'}">${r.alerta}</span></td>
                </tr>
            `).join('');
        }

        function actualizarGrafico(datos) {
            const ctx = document.getElementById('chart').getContext('2d');
            
            if (chart) chart.destroy();
            
            const ultimos = datos.slice(0, 10).reverse();
            const labels = ultimos.map(d => new Date(d.fecha).toLocaleTimeString());
            const tempData = ultimos.map(d => d.temperatura);
            const humData = ultimos.map(d => d.humedad);
            
            chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Temperatura (°C)',
                        data: tempData,
                        borderColor: '#ff6384',
                        backgroundColor: 'rgba(255, 99, 132, 0.1)',
                        fill: true,
                        tension: 0.4
                    }, {
                        label: 'Humedad (%)',
                        data: humData,
                        borderColor: '#36a2eb',
                        backgroundColor: 'rgba(54, 162, 235, 0.1)',
                        fill: true,
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { position: 'top' }
                    },
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });
        }

        // Inicialización
        window.addEventListener('load', function() {
            actualizar();
            setInterval(actualizar, 15000); // Actualizar cada 15 segundos
        });
    </script>
</body>
</html>
"""

# Template de pruebas
TEST_HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>🧪 Pruebas del Sistema</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f0f8ff; }
        .card { background: white; padding: 20px; margin: 15px 0; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        button { padding: 10px 20px; margin: 5px; border: none; border-radius: 5px; cursor: pointer; }
        .btn-primary { background: #007bff; color: white; }
        .btn-success { background: #28a745; color: white; }
        .btn-info { background: #17a2b8; color: white; }
        .success { color: #28a745; }
        .error { color: #dc3545; }
        .info { color: #17a2b8; }
    </style>
</head>
<body>
    <h1>🧪 Sistema de Pruebas - Invernadero</h1>
    
    <div class="card">
        <h3>📡 Estado de Conexión</h3>
        <p id="connectionStatus">Verificando...</p>
        <button class="btn-primary" onclick="testConnection()">Probar Conexión</button>
    </div>
    
    <div class="card">
        <h3>📊 Datos Actuales</h3>
        <div id="currentData">
            <p>Temperatura: <span id="temp">--</span></p>
            <p>Humedad: <span id="hum">--</span></p>
            <p>Bomba: <span id="bomba">--</span></p>
        </div>
        <button class="btn-success" onclick="getData()">Obtener Datos</button>
        <button class="btn-info" onclick="simulateData()">Simular Nuevos Datos</button>
    </div>
    
    <div class="card">
        <h3>🔧 Navegación</h3>
        <a href="/" class="btn-primary">🏠 Ir al Dashboard</a>
        <button class="btn-info" onclick="testAll()">🚀 Probar Todo</button>
    </div>
    
    <div class="card">
        <h3>📝 Log de Actividad</h3>
        <div id="log" style="height: 300px; overflow-y: auto; background: #f8f9fa; padding: 10px; border-radius: 4px; font-family: monospace;"></div>
    </div>

    <script>
        function log(message, type = 'info') {
            const logDiv = document.getElementById('log');
            const now = new Date().toLocaleTimeString();
            const colors = { info: '#17a2b8', success: '#28a745', error: '#dc3545' };
            logDiv.innerHTML += `<span style="color: ${colors[type]}">[${now}] ${message}</span><br>`;
            logDiv.scrollTop = logDiv.scrollHeight;
        }

        async function testConnection() {
            log('Probando conexión con el servidor...', 'info');
            try {
                const response = await fetch('/api/health');
                const data = await response.json();
                log('✅ Conexión exitosa: ' + data.message, 'success');
                document.getElementById('connectionStatus').innerHTML = '<span class="success">✅ Conectado - ' + data.server + '</span>';
                return true;
            } catch (error) {
                log('❌ Error de conexión: ' + error.message, 'error');
                document.getElementById('connectionStatus').innerHTML = '<span class="error">❌ Error: ' + error.message + '</span>';
                return false;
            }
        }

        async function getData() {
            log('Obteniendo datos del ambiente...', 'info');
            try {
                const response = await fetch('/api/estado/actual');
                const data = await response.json();
                
                if (data.ambiente) {
                    const amb = data.ambiente;
                    document.getElementById('temp').textContent = amb.temperatura + '°C';
                    document.getElementById('hum').textContent = amb.humedad + '%';
                    document.getElementById('bomba').textContent = amb.estado_bomba;
                    log(`📊 Datos actualizados - T: ${amb.temperatura}°C, H: ${amb.humedad}%`, 'success');
                } else {
                    log('⚠️ No se encontraron datos de ambiente', 'error');
                }
            } catch (error) {
                log('❌ Error obteniendo datos: ' + error.message, 'error');
            }
        }

        async function simulateData() {
            log('Simulando nuevos datos...', 'info');
            try {
                const response = await fetch('/api/simular_datos', { method: 'POST' });
                const data = await response.json();
                log('🎲 ' + data.message, 'success');
                setTimeout(getData, 1000);
            } catch (error) {
                log('❌ Error simulando datos: ' + error.message, 'error');
            }
        }

        async function testAll() {
            log('🚀 Iniciando prueba completa del sistema...', 'info');
            
            const connected = await testConnection();
            if (!connected) {
                log('❌ Prueba cancelada - sin conexión', 'error');
                return;
            }
            
            await new Promise(resolve => setTimeout(resolve, 1000));
            await getData();
            
            await new Promise(resolve => setTimeout(resolve, 1000));
            await simulateData();
            
            log('✅ Prueba completa finalizada', 'success');
        }

        window.onload = function() {
            log('🌿 Página de pruebas cargada', 'info');
            testConnection();
        };
    </script>
</body>
</html>
"""

def find_free_port():
    """Encuentra un puerto libre"""
    sock = socket.socket()
    sock.bind(('', 0))
    port = sock.getsockname()[1]
    sock.close()
    return port

if __name__ == '__main__':
    port = 5000
    try:
        # Intentar usar el puerto 5000, si no está libre usar otro
        sock = socket.socket()
        sock.bind(('127.0.0.1', port))
        sock.close()
    except OSError:
        port = find_free_port()
    
    print("🌿 SERVIDOR FLASK INVERNADERO")
    print("=" * 40)
    print(f"🚀 Dashboard: http://127.0.0.1:{port}")
    print(f"🧪 Pruebas: http://127.0.0.1:{port}/test")
    print(f"📡 API: http://127.0.0.1:{port}/api/health")
    print("=" * 40)
    
    app.run(host='127.0.0.1', port=port, debug=False, threaded=True)