import requests
import json
from datetime import datetime

# Datos de prueba 1
data1 = {
    'temperatura': 25.5,
    'humedad': 65.0,
    'estado_bomba': 'Apagada',
    'alerta': 'Normal'
}

# Datos de prueba 2
data2 = {
    'temperatura': 27.2,
    'humedad': 58.0,
    'estado_bomba': 'Apagada', 
    'alerta': 'Normal'
}

# Datos de prueba 3
data3 = {
    'temperatura': 23.8,
    'humedad': 72.0,
    'estado_bomba': 'Encendida',
    'alerta': 'Medio'
}

datasets = [data1, data2, data3]

for i, data in enumerate(datasets, 1):
    try:
        response = requests.post('http://localhost:5000/api/ambiente', 
                               json=data,
                               headers={'Content-Type': 'application/json'},
                               timeout=5)
        print(f'Datos {i} - Status: {response.status_code}')
        if response.status_code != 200:
            print(f'Response: {response.text}')
    except Exception as e:
        print(f'Error en datos {i}: {str(e)}')

print('\nProbando obtener el estado actual...')
try:
    response = requests.get('http://localhost:5000/api/estado/actual', timeout=5)
    print(f'Estado actual - Status: {response.status_code}')
    if response.status_code == 200:
        data = response.json()
        print(f'Ambiente: {data.get("ambiente", "No disponible")}')
    else:
        print(f'Response: {response.text}')
except Exception as e:
    print(f'Error obteniendo estado: {str(e)}')

print('\nProbando obtener datos de ambiente...')
try:
    response = requests.get('http://localhost:5000/api/ambiente?limit=20', timeout=5)
    print(f'API ambiente - Status: {response.status_code}')
    if response.status_code == 200:
        data = response.json()
        print(f'Registros obtenidos: {len(data)}')
        for registro in data[:3]:  # Mostrar solo los primeros 3
            print(f'  - Fecha: {registro.get("fecha")}, Temp: {registro.get("temperatura")}°C, Hum: {registro.get("humedad")}%')
    else:
        print(f'Response: {response.text}')
except Exception as e:
    print(f'Error obteniendo ambiente: {str(e)}')