import urllib.request
import urllib.parse
import json

def test_api():
    print("🧪 Probando la API del invernadero con urllib...")
    
    # Probar salud de la API
    try:
        with urllib.request.urlopen('http://localhost:5000/api/health') as response:
            data = json.loads(response.read())
            print(f"✅ API Health - Status: {response.status}")
            print(f"   Mensaje: {data.get('message', 'N/A')}")
    except Exception as e:
        print(f"❌ Error en health check: {e}")
        return
    
    # Probar estado actual
    try:
        with urllib.request.urlopen('http://localhost:5000/api/estado/actual') as response:
            data = json.loads(response.read())
            print(f"✅ Estado Actual - Status: {response.status}")
            ambiente = data.get('ambiente', {})
            eventos = data.get('eventos', [])
            print(f"   Ambiente: Temp: {ambiente.get('temperatura', 'N/A')}°C, Hum: {ambiente.get('humedad', 'N/A')}%")
            print(f"   Eventos registrados: {len(eventos)}")
    except Exception as e:
        print(f"❌ Error obteniendo estado actual: {e}")
        return
    
    # Simular nuevos datos
    try:
        data = json.dumps({}).encode('utf-8')
        req = urllib.request.Request(
            'http://localhost:5000/api/simular_datos',
            data=data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read())
            print(f"✅ Simulación de datos - Status: {response.status}")
            nuevo = result.get('nuevo_registro', {})
            print(f"   Nuevos datos: Temp: {nuevo.get('temperatura', 'N/A')}°C, Hum: {nuevo.get('humedad', 'N/A')}%")
    except Exception as e:
        print(f"❌ Error simulando datos: {e}")
    
    # Verificar datos de ambiente después de la simulación
    try:
        with urllib.request.urlopen('http://localhost:5000/api/ambiente?limit=3') as response:
            data = json.loads(response.read())
            print(f"✅ API Ambiente - Status: {response.status}")
            print(f"   Registros encontrados: {len(data)}")
            for i, registro in enumerate(data[:3]):
                print(f"   {i+1}. Fecha: {registro.get('fecha')}, Temp: {registro.get('temperatura')}°C, Hum: {registro.get('humedad')}%")
    except Exception as e:
        print(f"❌ Error obteniendo ambiente: {e}")
    
    print("\n🔥 Prueba finalizada - Ahora revisa la interfaz web!")

if __name__ == "__main__":
    test_api()