#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
✅ SISTEMA LISTO PARA ARDUINO ESP32 - PRUEBA FINAL
==================================================
Script de prueba final para verificar que todo funciona correctamente
"""

import requests
import json
from datetime import datetime
import sys

# Configuración
SERVER_URL = "http://127.0.0.1:5000"

def test_health():
    """Probar endpoint de salud"""
    try:
        response = requests.get(f"{SERVER_URL}/api/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Servidor: {data['status']}")
            print(f"✅ Base de datos: {data['database']}")
            print(f"✅ IP local: {data['local_ip']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error conectando al servidor: {e}")
        return False

def test_arduino_endpoint():
    """Probar endpoint que usará el Arduino"""
    try:
        # Datos de prueba como los enviará el Arduino
        datos_arduino = {
            "temperatura": 24.8,
            "humedad": 67.3,
            "estado_bomba": "Encendida",
            "alerta": "Normal"
        }
        
        response = requests.post(
            f"{SERVER_URL}/api/sensores/ambiente",
            json=datos_arduino,
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        
        if response.status_code == 201:
            print(f"✅ Endpoint Arduino funcional: datos recibidos correctamente")
            result = response.json()
            print(f"   📅 Timestamp: {result.get('timestamp', 'N/A')}")
            return True
        else:
            print(f"❌ Error en endpoint Arduino: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error probando endpoint Arduino: {e}")
        return False

def test_data_retrieval():
    """Probar que se pueden obtener los datos"""
    try:
        response = requests.get(f"{SERVER_URL}/api/ambiente")
        if response.status_code == 200:
            data = response.json()
            if data.get('ultimo_registro'):
                ultimo = data['ultimo_registro']
                print(f"✅ Datos recuperados correctamente:")
                print(f"   🌡️ Temperatura: {ultimo.get('temperatura', 'N/A')}°C")
                print(f"   💧 Humedad: {ultimo.get('humedad', 'N/A')}%")
                print(f"   💡 Bomba: {ultimo.get('estado_bomba', 'N/A')}")
                print(f"   🚨 Alerta: {ultimo.get('alerta', 'N/A')}")
                return True
            else:
                print(f"⚠️ No hay datos en la base de datos aún")
                return True
        else:
            print(f"❌ Error obteniendo datos: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error recuperando datos: {e}")
        return False

def main():
    """Función principal de prueba"""
    print("🧪 PRUEBA FINAL DEL SISTEMA PARA ARDUINO ESP32")
    print("=" * 50)
    print(f"🎯 Servidor: {SERVER_URL}")
    print(f"⏰ Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Contadores de pruebas
    pruebas_pasadas = 0
    total_pruebas = 3
    
    # Prueba 1: Health check
    print("📡 Prueba 1: Verificando servidor...")
    if test_health():
        pruebas_pasadas += 1
    print()
    
    # Prueba 2: Endpoint Arduino
    print("🤖 Prueba 2: Probando endpoint del Arduino...")
    if test_arduino_endpoint():
        pruebas_pasadas += 1
    print()
    
    # Prueba 3: Recuperación de datos
    print("📊 Prueba 3: Verificando recuperación de datos...")
    if test_data_retrieval():
        pruebas_pasadas += 1
    print()
    
    # Resultado final
    print("=" * 50)
    print(f"📈 RESULTADO: {pruebas_pasadas}/{total_pruebas} pruebas pasadas")
    
    if pruebas_pasadas == total_pruebas:
        print("🎉 ¡SISTEMA COMPLETAMENTE LISTO PARA ARDUINO ESP32!")
        print()
        print("📋 PRÓXIMOS PASOS:")
        print("   1. Configurar Arduino con tu WiFi")
        print("   2. Cambiar serverURL en Arduino a: http://192.168.1.7:5000")
        print("   3. Compilar y subir código al ESP32")
        print("   4. Verificar en monitor serie la conexión WiFi")
        print("   5. Abrir dashboard: http://192.168.1.7:5000")
        print()
        print("🌐 URLs importantes:")
        print(f"   • Dashboard: http://192.168.1.7:5000")
        print(f"   • Configuración: http://192.168.1.7:5000/config")
        print(f"   • API Health: http://192.168.1.7:5000/api/health")
        return 0
    else:
        print("❌ Hay problemas que necesitan resolverse antes de conectar el Arduino")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)