#!/usr/bin/env python3
"""
Servidor web ultra-simple para demostrar la interfaz del invernadero
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
import os
from datetime import datetime, timedelta
import random

# Datos simulados en memoria
datos_ambiente = [
    {
        'id': 1,
        'fecha': '2025-10-23 18:30:00',
        'temperatura': 25.5,
        'humedad': 65.0,
        'estado_bomba': 'Apagada',
        'alerta': 'Normal'
    },
    {
        'id': 2,
        'fecha': '2025-10-23 18:25:00',
        'temperatura': 27.2,
        'humedad': 58.0,
        'estado_bomba': 'Apagada',
        'alerta': 'Normal'
    },
    {
        'id': 3,
        'fecha': '2025-10-23 18:20:00',
        'temperatura': 23.8,
        'humedad': 72.0,
        'estado_bomba': 'Encendida',
        'alerta': 'Medio'
    },
    {
        'id': 4,
        'fecha': '2025-10-23 18:15:00',
        'temperatura': 26.1,
        'humedad': 62.0,
        'estado_bomba': 'Apagada',
        'alerta': 'Normal'
    },
    {
        'id': 5,
        'fecha': '2025-10-23 18:10:00',
        'temperatura': 24.7,
        'humedad': 68.0,
        'estado_bomba': 'Apagada',
        'alerta': 'Normal'
    }
]

class InvernaderoHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        """Sobrescribir para mostrar logs más claros"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"🌐 [{timestamp}] {format % args}")

    def do_GET(self):
        """Manejar peticiones GET"""
        path = self.path.split('?')[0]
        print(f"📥 Recibida petición GET: {path}")
        
        # Agregar CORS headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json' if path.startswith('/api/') else 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        if path == '/api/health':
            response = {
                'status': 'ok',
                'timestamp': datetime.now().isoformat(),
                'message': 'Sistema de invernadero funcionando (servidor HTTP nativo)',
                'server': 'Python HTTP Server',
                'port': 8000
            }
            
        elif path == '/api/ambiente':
            # Parsear parámetros de consulta
            query_params = urllib.parse.parse_qs(self.path.split('?')[1] if '?' in self.path else '')
            limit = int(query_params.get('limit', [20])[0])
            response = datos_ambiente[:limit]
            
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
            
        elif path == '/' or path == '/index.html':
            # Servir la página principal
            try:
                static_path = os.path.join(os.path.dirname(__file__), 'backend', 'static', 'main.html')
                with open(static_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.wfile.write(content.encode('utf-8'))
                    return
            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'Archivo main.html no encontrado en backend/static/')
                return
                
        elif path == '/debug.html':
            # Servir la página de debug
            try:
                static_path = os.path.join(os.path.dirname(__file__), 'backend', 'static', 'debug.html')
                with open(static_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Reemplazar las rutas de la API para usar el puerto 8000
                    content = content.replace("fetch('/api/", "fetch('http://localhost:8000/api/")
                    self.wfile.write(content.encode('utf-8'))
                    return
            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'Archivo debug.html no encontrado en backend/static/')
                return
        else:
            response = {'error': 'Endpoint no encontrado', 'path': path}
        
        # Enviar respuesta JSON
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
    
    def do_POST(self):
        """Manejar peticiones POST"""
        if self.path == '/api/simular_datos':
            # Simular nuevos datos
            nuevo_registro = {
                'id': len(datos_ambiente) + 1,
                'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'temperatura': round(random.uniform(20.0, 30.0), 1),
                'humedad': round(random.uniform(40.0, 80.0), 1),
                'estado_bomba': random.choice(['Encendida', 'Apagada']),
                'alerta': random.choice(['Normal', 'Normal', 'Normal', 'Medio'])
            }
            datos_ambiente.insert(0, nuevo_registro)
            
            # Mantener solo los últimos 50 registros
            if len(datos_ambiente) > 50:
                datos_ambiente[:] = datos_ambiente[:50]
            
            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                'message': 'Datos simulados agregados correctamente',
                'nuevo_registro': nuevo_registro
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        """Manejar preflight CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def main():
    server_address = ('127.0.0.1', 8000)
    httpd = HTTPServer(server_address, InvernaderoHandler)
    
    print("🌿 Servidor HTTP Simple del Invernadero")
    print("=" * 50)
    print(f"🚀 Ejecutándose en: http://127.0.0.1:8000")
    print("📊 Dashboard: http://127.0.0.1:8000")
    print("🔧 Debug: http://127.0.0.1:8000/debug.html")
    print("📡 API Health: http://127.0.0.1:8000/api/health")
    print("📈 Datos en memoria (sin base de datos)")
    print("=" * 50)
    print("Presiona Ctrl+C para detener")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido")
        httpd.server_close()

if __name__ == '__main__':
    main()