#!/usr/bin/env python3
"""
Script de diagnóstico directo para el servidor Flask
"""

import urllib.request
import urllib.error
import json
import time

def test_url(url, method='GET', data=None):
    """Probar una URL específica"""
    try:
        if data:
            data = json.dumps(data).encode('utf-8') if isinstance(data, dict) else data.encode('utf-8')
            
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read().decode('utf-8')
            return {
                'success': True,
                'status': response.status,
                'content': content,
                'headers': dict(response.headers)
            }
    except urllib.error.HTTPError as e:
        return {
            'success': False,
            'status': e.code,
            'content': e.read().decode('utf-8') if hasattr(e, 'read') else str(e),
            'error': f'HTTP Error {e.code}'
        }
    except Exception as e:
        return {
            'success': False,
            'status': 0,
            'content': '',
            'error': str(e)
        }

def main():
    base_url = 'http://127.0.0.1:5001'
    
    tests = [
        ('Health Check', f'{base_url}/api/health', 'GET'),
        ('Estado Actual', f'{base_url}/api/estado/actual', 'GET'),
        ('Datos Ambiente', f'{base_url}/api/ambiente?limit=5', 'GET'),
        ('Página Principal', f'{base_url}/', 'GET'),
        ('Página Debug', f'{base_url}/debug.html', 'GET')
    ]
    
    print("🔍 Iniciando diagnóstico de conectividad...\n")
    
    for name, url, method in tests:
        print(f"🧪 Probando: {name}")
        print(f"   URL: {url}")
        
        result = test_url(url, method)
        
        if result['success']:
            print(f"   ✅ Status: {result['status']}")
            if 'application/json' in result.get('headers', {}).get('Content-Type', ''):
                try:
                    data = json.loads(result['content'])
                    if name == 'Estado Actual' and 'ambiente' in data:
                        amb = data['ambiente']
                        if amb:
                            print(f"   📊 Temp: {amb.get('temperatura')}°C, Hum: {amb.get('humedad')}%")
                        else:
                            print(f"   ⚠️ Sin datos de ambiente")
                    elif name == 'Datos Ambiente' and isinstance(data, list):
                        print(f"   📈 Registros: {len(data)}")
                        if data:
                            print(f"   🔍 Último: {data[0].get('fecha')} - {data[0].get('temperatura')}°C")
                    elif name == 'Health Check':
                        print(f"   💚 {data.get('message', 'OK')}")
                except:
                    print(f"   📄 Contenido: {result['content'][:100]}...")
            else:
                print(f"   📄 Tamaño: {len(result['content'])} bytes")
        else:
            print(f"   ❌ Error: {result['error']}")
            if result['content']:
                print(f"   📄 Respuesta: {result['content'][:200]}...")
        
        print()
        time.sleep(1)
    
    print("🏁 Diagnóstico completado")

if __name__ == '__main__':
    main()