#!/usr/bin/env python3
"""Script para agregar datos de prueba al invernadero"""

import json
from urllib.request import urlopen, Request
from urllib.parse import urlencode

def enviar_datos():
    """Enviar datos de prueba al servidor"""
    url = 'http://127.0.0.1:5000/api/sensores/ambiente'
    
    datos = {
        'temperatura': 24.5,
        'humedad': 68.2,
        'estado_bomba': 'Encendida',
        'alerta': 'Normal'
    }
    
    try:
        # Crear la petición
        data = json.dumps(datos).encode('utf-8')
        req = Request(url, data=data)
        req.add_header('Content-Type', 'application/json')
        
        # Enviar
        response = urlopen(req)
        result = response.read().decode('utf-8')
        print(f"✅ Datos enviados correctamente: {result}")
        
        # Agregar más datos
        for i in range(5):
            datos['temperatura'] = 20.0 + (i * 2.5)
            datos['humedad'] = 60.0 + (i * 3.0)
            data = json.dumps(datos).encode('utf-8')
            req = Request(url, data=data)
            req.add_header('Content-Type', 'application/json')
            response = urlopen(req)
            print(f"✅ Dato {i+1} agregado: Temp={datos['temperatura']}°C, Hum={datos['humedad']}%")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🌿 Agregando datos de prueba al invernadero...")
    enviar_datos()
    print("✅ Proceso completado. Refresca la interfaz web.")