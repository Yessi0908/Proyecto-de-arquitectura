#!/usr/bin/env python3
"""
Aplicación Flask simplificada para el sistema de invernadero
Versión de demostración sin base de datos (usando datos en memoria)
"""

import json
import os
import time
from datetime import datetime, timedelta
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

# Datos simulados en memoria
datos_ambiente = [
    {
        'id': 1,
        'fecha': '2025-10-23 17:30:00',
        'temperatura': 25.5,
        'humedad': 65.0,
        'estado_bomba': 'Apagada',
        'alerta': 'Normal'
    },
    {
        'id': 2,
        'fecha': '2025-10-23 17:25:00',
        'temperatura': 27.2,
        'humedad': 58.0,
        'estado_bomba': 'Apagada',
        'alerta': 'Normal'
    },
    {
        'id': 3,
        'fecha': '2025-10-23 17:20:00',
        'temperatura': 23.8,
        'humedad': 72.0,
        'estado_bomba': 'Encendida',
        'alerta': 'Medio'
    },
    {
        'id': 4,
        'fecha': '2025-10-23 17:15:00',
        'temperatura': 26.1,
        'humedad': 62.0,
        'estado_bomba': 'Apagada',
        'alerta': 'Normal'
    },
    {
        'id': 5,
        'fecha': '2025-10-23 17:10:00',
        'temperatura': 24.7,
        'humedad': 68.0,
        'estado_bomba': 'Apagada',
        'alerta': 'Normal'
    }
]

datos_seguridad = [
    {
        'id': 1,
        'fecha': '2025-10-23 17:25:00',
        'tipo_evento': 'Movimiento',
        'descripcion': 'Movimiento detectado en zona norte',
        'nivel_alerta': 'Medio'
    }
]

datos_acceso = [
    {
        'id': 1,
        'fecha': '2025-10-23 17:20:00',
        'persona': 'Juan Pérez',
        'acceso_autorizado': True
    }
]

# Inicializar Flask
app = Flask(__name__, static_folder='static', static_url_path='/')
CORS(app)

@app.route('/')
def index():
    """Servir la página principal"""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/health')
def health():
    """Verificación de salud del API"""
    return jsonify({
        'status': 'ok', 
        'timestamp': datetime.now().isoformat(),
        'message': 'Sistema de invernadero funcionando (modo demo)'
    })

@app.route('/api/ambiente', methods=['GET', 'POST'])
def handle_ambiente():
    """Manejar registros de ambiente"""
    global datos_ambiente
    
    if request.method == 'POST':
        # Agregar nuevo registro
        data = request.get_json()
        nuevo_registro = {
            'id': len(datos_ambiente) + 1,
            'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'temperatura': data.get('temperatura'),
            'humedad': data.get('humedad'),
            'estado_bomba': data.get('estado_bomba', 'Apagada'),
            'alerta': data.get('alerta', 'Normal')
        }
        datos_ambiente.insert(0, nuevo_registro)  # Agregar al principio
        # Mantener solo los últimos 50 registros
        if len(datos_ambiente) > 50:
            datos_ambiente = datos_ambiente[:50]
        return jsonify(nuevo_registro), 201
    
    # GET: Obtener registros con filtros
    limit = request.args.get('limit', 20, type=int)
    desde = request.args.get('desde')
    hasta = request.args.get('hasta')
    
    resultados = datos_ambiente.copy()
    
    # Aplicar filtros de fecha si se especifican
    if desde or hasta:
        resultados_filtrados = []
        for registro in resultados:
            fecha_registro = datetime.strptime(registro['fecha'], '%Y-%m-%d %H:%M:%S')
            if desde:
                fecha_desde = datetime.fromisoformat(desde.replace('T', ' '))
                if fecha_registro < fecha_desde:
                    continue
            if hasta:
                fecha_hasta = datetime.fromisoformat(hasta.replace('T', ' '))
                if fecha_registro > fecha_hasta:
                    continue
            resultados_filtrados.append(registro)
        resultados = resultados_filtrados
    
    # Aplicar límite
    resultados = resultados[:limit]
    
    return jsonify(resultados)

@app.route('/api/seguridad', methods=['GET'])
def get_seguridad():
    """Obtener registros de seguridad"""
    limit = request.args.get('limit', 20, type=int)
    return jsonify(datos_seguridad[:limit])

@app.route('/api/accesos', methods=['GET'])
def get_accesos():
    """Obtener registros de acceso"""
    limit = request.args.get('limit', 20, type=int)
    return jsonify(datos_acceso[:limit])

@app.route('/api/estado/actual', methods=['GET'])
def get_estado_actual():
    """Obtener el estado actual de todos los módulos"""
    # Obtener los registros más recientes
    ambiente = datos_ambiente[0] if datos_ambiente else None
    seguridad = datos_seguridad[0] if datos_seguridad else None
    acceso = datos_acceso[0] if datos_acceso else None
    
    # Eventos recientes combinados
    eventos = []
    
    # Agregar eventos de ambiente (últimos 5)
    for registro in datos_ambiente[:5]:
        eventos.append({
            'fecha': registro['fecha'],
            'tipo': 'Ambiente',
            'descripcion': f"T:{registro['temperatura']}°C H:{registro['humedad']}%",
            'nivel': registro['alerta']
        })
    
    # Agregar eventos de seguridad (últimos 5)
    for registro in datos_seguridad[:5]:
        eventos.append({
            'fecha': registro['fecha'],
            'tipo': registro['tipo_evento'],
            'descripcion': registro['descripcion'],
            'nivel': registro['nivel_alerta']
        })
    
    # Ordenar por fecha (más reciente primero)
    eventos.sort(key=lambda x: x['fecha'], reverse=True)
    eventos = eventos[:10]  # Solo los últimos 10
    
    return jsonify({
        'ambiente': ambiente,
        'seguridad': seguridad,
        'acceso': acceso,
        'eventos': eventos
    })

@app.route('/api/config/umbrales', methods=['GET', 'POST'])
def config_umbrales():
    """Configuración de umbrales del sistema"""
    if request.method == 'GET':
        return jsonify({
            'temperatura': {
                'min': 18.0,
                'max': 28.0,
                'critica': 35.0
            },
            'humedad': {
                'min': 40.0,
                'max': 80.0,
                'critica': 90.0
            },
            'humo': {
                'umbral': 300,
                'critico': 500
            }
        })
    
    # POST: Guardar configuración (en memoria para esta demo)
    config = request.get_json()
    return jsonify({'message': 'Configuración guardada correctamente (modo demo)'}), 200

@app.route('/api/simular_datos', methods=['POST'])
def simular_datos():
    """Endpoint para simular nuevos datos de sensores"""
    global datos_ambiente, datos_seguridad, datos_acceso
    
    import random
    
    # Simular datos de ambiente
    nuevo_ambiente = {
        'id': len(datos_ambiente) + 1,
        'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'temperatura': round(random.uniform(20.0, 30.0), 1),
        'humedad': round(random.uniform(40.0, 80.0), 1),
        'estado_bomba': random.choice(['Encendida', 'Apagada']),
        'alerta': random.choice(['Normal', 'Normal', 'Normal', 'Medio'])  # 75% Normal
    }
    
    datos_ambiente.insert(0, nuevo_ambiente)
    
    # Mantener solo los últimos 50 registros
    if len(datos_ambiente) > 50:
        datos_ambiente = datos_ambiente[:50]
    
    return jsonify({
        'message': 'Datos simulados agregados correctamente',
        'nuevo_registro': nuevo_ambiente
    }), 201

if __name__ == '__main__':
    print("🌿 Iniciando Sistema de Invernadero IoT (Modo Demo)...")
    print("📊 Dashboard disponible en: http://localhost:5000")
    print("🔧 API Health Check: http://localhost:5000/api/health")
    print("🎮 Simular datos: POST http://localhost:5000/api/simular_datos")
    print("📈 Datos en memoria - Sin base de datos requerida")
    
    app.run(host='127.0.0.1', port=5000, debug=False)