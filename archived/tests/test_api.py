import requests
import json

print("🧪 Probando la API del invernadero...")

# Probar salud de la API
try:
    response = requests.get('http://localhost:5000/api/health', timeout=5)
    print(f"✅ API Health - Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Mensaje: {data.get('message', 'N/A')}")
except Exception as e:
    print(f"❌ Error en health check: {e}")

# Probar datos de ambiente
try:
    response = requests.get('http://localhost:5000/api/ambiente?limit=5', timeout=5)
    print(f"✅ API Ambiente - Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Registros encontrados: {len(data)}")
        if data:
            print(f"   Último registro: Temp: {data[0].get('temperatura')}°C, Hum: {data[0].get('humedad')}%")
except Exception as e:
    print(f"❌ Error obteniendo ambiente: {e}")

# Probar estado actual
try:
    response = requests.get('http://localhost:5000/api/estado/actual', timeout=5)
    print(f"✅ Estado Actual - Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        ambiente = data.get('ambiente', {})
        eventos = data.get('eventos', [])
        print(f"   Ambiente: Temp: {ambiente.get('temperatura', 'N/A')}°C")
        print(f"   Eventos registrados: {len(eventos)}")
except Exception as e:
    print(f"❌ Error obteniendo estado actual: {e}")

print("\n🔥 Prueba finalizada")