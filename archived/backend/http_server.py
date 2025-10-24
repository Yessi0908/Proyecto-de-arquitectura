#!/usr/bin/env python3
"""
Servidor web ultra-simple para el sistema de invernadero
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
from datetime import datetime

# Datos simulados
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
    }
]

class InvernaderoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split('?')[0]
        
        # Agregar CORS headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        if path == '/api/health':
            response = {
                'status': 'ok',
                'timestamp': datetime.now().isoformat(),
                'message': 'Sistema de invernadero funcionando (servidor simple)'
            }
            
        elif path == '/api/ambiente':
            response = datos_ambiente
            
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
                    } for r in datos_ambiente[:5]
                ]
            }
        else:
            response = {'error': 'Endpoint no encontrado'}
        
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
    
    def do_POST(self):
        # Solo manejar simulación de datos
        if self.path == '/api/simular_datos':
            import random
            nuevo_registro = {
                'id': len(datos_ambiente) + 1,
                'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'temperatura': round(random.uniform(20.0, 30.0), 1),
                'humedad': round(random.uniform(40.0, 80.0), 1),
                'estado_bomba': random.choice(['Encendida', 'Apagada']),
                'alerta': random.choice(['Normal', 'Normal', 'Normal', 'Medio'])
            }
            datos_ambiente.insert(0, nuevo_registro)
            
            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                'message': 'Datos simulados agregados',
                'nuevo_registro': nuevo_registro
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        # Manejar preflight CORS
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == '__main__':
    server_address = ('127.0.0.1', 5000)
    httpd = HTTPServer(server_address, InvernaderoHandler)
    
    print("🌿 Servidor simple de invernadero iniciado")
    print("📊 Dashboard: http://localhost:5000")
    print("🔧 API Health: http://localhost:5000/api/health")
    print("📈 Usando servidor HTTP nativo de Python")
    print(f"🚀 Servidor ejecutándose en {server_address[0]}:{server_address[1]}")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido")
        httpd.server_close()