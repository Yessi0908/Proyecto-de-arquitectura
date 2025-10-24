#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 SIMULADOR DE ARDUINO ESP32 - PRUEBAS
========================================
Script para probar que el servidor funciona correctamente
antes de conectar el Arduino real
"""

import requests
import json
import time
import random
from datetime import datetime

# Configuración del servidor
SERVER_URL = "http://192.168.1.7:5000"
ENDPOINT_AMBIENTE = f"{SERVER_URL}/api/sensores/ambiente"
ENDPOINT_SEGURIDAD = f"{SERVER_URL}/api/sensores/seguridad"

def simular_datos_arduino():
    """Simula datos como los enviaría el Arduino ESP32"""
    
    # Generar datos simulados realistas
    temperatura = round(random.uniform(18.0, 32.0), 1)
    humedad = round(random.uniform(45.0, 85.0), 1)
    
    # Estado de bomba basado en humedad
    estado_bomba = "Encendida" if humedad < 60 else "Apagada"
    
    # Nivel de alerta basado en condiciones
    if temperatura > 30 or humedad < 50 or humedad > 80:
        alerta = "Alto" if temperatura > 32 or humedad < 45 else "Medio"
    else:
        alerta = "Normal"
    
    datos = {
        "temperatura": temperatura,
        "humedad": humedad,
        "estado_bomba": estado_bomba,
        "alerta": alerta
    }
    
    return datos

def enviar_datos_ambiente(datos):
    """Enviar datos de ambiente al servidor"""
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(ENDPOINT_AMBIENTE, json=datos, headers=headers, timeout=5)
        
        if response.status_code == 201:
            print(f"✅ Datos enviados: {datos['temperatura']}°C, {datos['humedad']}%, {datos['estado_bomba']}, {datos['alerta']}")
            return True
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error enviando datos: {e}")
        return False

def enviar_alerta_seguridad(tipo, descripcion, nivel):
    """Enviar alerta de seguridad"""
    try:
        datos = {
            "tipo_evento": tipo,
            "descripcion": descripcion,
            "nivel_alerta": nivel
        }
        
        headers = {'Content-Type': 'application/json'}
        response = requests.post(ENDPOINT_SEGURIDAD, json=datos, headers=headers, timeout=5)
        
        if response.status_code == 201:
            print(f"🚨 Alerta enviada: {tipo} - {nivel}")
            return True
        else:
            print(f"❌ Error enviando alerta {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error enviando alerta: {e}")
        return False

def verificar_servidor():
    """Verificar que el servidor esté funcionando"""
    try:
        response = requests.get(f"{SERVER_URL}/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Servidor activo: {data['message']}")
            print(f"📡 Base de datos: {data['database']}")
            return True
        else:
            print(f"❌ Servidor no responde: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error conectando al servidor: {e}")
        return False

def main():
    """Función principal del simulador"""
    print("🧪 SIMULADOR DE ARDUINO ESP32")
    print("=" * 40)
    print(f"🎯 Servidor objetivo: {SERVER_URL}")
    print("=" * 40)
    
    # Verificar servidor
    if not verificar_servidor():
        print("❌ No se puede conectar al servidor. Verifica que esté ejecutándose.")
        return
    
    print(f"🚀 Iniciando simulación... (Ctrl+C para detener)")
    print(f"📊 Dashboard: {SERVER_URL}")
    print()
    
    contador = 0
    
    try:
        while True:
            contador += 1
            ahora = datetime.now().strftime("%H:%M:%S")
            
            print(f"[{ahora}] Ciclo #{contador}")
            
            # Enviar datos de ambiente cada ciclo
            datos = simular_datos_arduino()
            if enviar_datos_ambiente(datos):
                
                # Enviar alerta ocasional de seguridad (10% de probabilidad)
                if random.random() < 0.1:
                    alertas = [
                        ("Movimiento", "Movimiento detectado en el invernadero", "Bajo"),
                        ("Humo", "Nivel de humo ligeramente elevado", "Medio"),
                        ("Temperatura", "Temperatura por encima del rango normal", "Alto")
                    ]
                    alerta = random.choice(alertas)
                    enviar_alerta_seguridad(alerta[0], alerta[1], alerta[2])
            
            print(f"⏳ Esperando 30 segundos... (como el Arduino real)")
            print("-" * 40)
            
            # Esperar 30 segundos como el Arduino real
            time.sleep(30)
            
    except KeyboardInterrupt:
        print(f"\n🛑 Simulación detenida por el usuario")
        print(f"📊 Total de ciclos ejecutados: {contador}")
        print(f"🌐 Revisa el dashboard en: {SERVER_URL}")

if __name__ == "__main__":
    main()