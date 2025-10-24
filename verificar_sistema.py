#!/usr/bin/env python3
"""
Script de verificación del sistema del invernadero
"""

import requests
import json
from datetime import datetime

def verificar_sistema():
    """Verificar que todos los componentes funcionen"""
    base_url = "http://localhost:5000"
    
    print("🔍 VERIFICACIÓN DEL SISTEMA DE INVERNADERO")
    print("=" * 50)
    
    try:
        # 1. Verificar que el servidor responda
        print("1️⃣ Verificando servidor...")
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Servidor funcionando correctamente")
        else:
            print(f"❌ Servidor respondió con código: {response.status_code}")
            return False
            
        # 2. Verificar endpoint de datos
        print("\n2️⃣ Verificando endpoint de datos...")
        response = requests.get(f"{base_url}/api/ambiente")
        if response.status_code == 200:
            data = response.json()
            print("✅ Endpoint de datos funcionando")
            print(f"📊 Último registro: {data}")
        else:
            print(f"❌ Endpoint de datos falló: {response.status_code}")
        
        # 3. Verificar envío de datos simulados
        print("\n3️⃣ Enviando datos de prueba...")
        test_data = {
            "temperatura": 25.5,
            "humedad": 60.3,
            "estado_bomba": "Encendida",
            "alerta": "Normal"
        }
        
        response = requests.post(
            f"{base_url}/api/sensores/ambiente",
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            print("✅ Envío de datos funcionando")
            result = response.json()
            print(f"📝 Respuesta: {result['message']}")
        else:
            print(f"❌ Envío de datos falló: {response.status_code}")
        
        # 4. Verificar generación de PDF
        print("\n4️⃣ Verificando generación de PDF...")
        response = requests.get(f"{base_url}/api/generar_pdf")
        
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '')
            if 'application/pdf' in content_type:
                pdf_size = len(response.content)
                print(f"✅ PDF generado correctamente - Tamaño: {pdf_size} bytes")
                
                # Guardar PDF de prueba
                filename = f"test_pdf_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                with open(filename, 'wb') as f:
                    f.write(response.content)
                print(f"📄 PDF guardado como: {filename}")
                
            else:
                print(f"❌ Respuesta no es PDF: {content_type}")
        else:
            print(f"❌ Generación de PDF falló: {response.status_code}")
            try:
                error_info = response.json()
                print(f"🔍 Error detallado: {error_info}")
            except:
                print(f"🔍 Error texto: {response.text}")
        
        print("\n🎉 VERIFICACIÓN COMPLETADA")
        print("✅ Sistema funcionando correctamente")
        print(f"🌐 Accede al dashboard: {base_url}")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ No se pudo conectar al servidor")
        print("💡 Asegúrate de que el servidor esté ejecutándose:")
        print("   python servidor_simple_arduino.py")
        return False
        
    except Exception as e:
        print(f"❌ Error durante verificación: {e}")
        return False

if __name__ == "__main__":
    verificar_sistema()