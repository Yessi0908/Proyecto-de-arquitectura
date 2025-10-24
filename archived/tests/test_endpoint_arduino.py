#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prueba rápida del endpoint Arduino
"""

import requests
import json

def test_arduino_endpoint():
    """Probar que el Arduino puede enviar datos"""
    try:
        # Datos que enviará el Arduino
        datos = {
            "temperatura": 25.6,
            "humedad": 70.2,
            "estado_bomba": "Encendida",
            "alerta": "Normal"
        }
        
        # Enviar datos
        response = requests.post(
            'http://127.0.0.1:5000/api/sensores/ambiente',
            json=datos,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 201:
            print("✅ Endpoint Arduino funciona correctamente")
            print(f"📡 Datos enviados: {datos}")
            print(f"📤 Respuesta: {response.json()}")
            return True
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 PRUEBA DEL ENDPOINT ARDUINO")
    print("=" * 30)
    test_arduino_endpoint()