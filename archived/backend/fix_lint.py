#!/usr/bin/env python3
"""
Script para corregir errores de linting en app.py
"""

import re

def fix_app_py():
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Corregir F841: variable 'data' no utilizada
    content = re.sub(r'        data = request\.get_json\(\)\s*\n', '', content)
    
    # Corregir F541: f-string sin placeholders
    content = content.replace("print(f'⚠️  Sistema iniciado sin base de datos')", 
                             "print('⚠️  Sistema iniciado sin base de datos')")
    content = content.replace("print(f'🌱 Servidor Flask iniciado en modo desarrollo')", 
                             "print('🌱 Servidor Flask iniciado en modo desarrollo')")
    content = content.replace("print(f'🔗 Dashboard disponible en: http://localhost:5000')", 
                             "print('🔗 Dashboard disponible en: http://localhost:5000')")
    content = content.replace("print(f'📖 API docs disponibles en: http://localhost:5000/api')", 
                             "print('📖 API docs disponibles en: http://localhost:5000/api')")
    
    # Arreglar líneas demasiado largas dividiendo cadenas
    long_lines = [
        ('return jsonify({"mensaje": "Registro de ambiente guardado correctamente", "id": cur.lastrowid})',
         'return jsonify({"mensaje": "Registro de ambiente guardado correctamente", '
         '"id": cur.lastrowid})'),
        
        ('{"mensaje": "Control de riego actualizado", "estado": estado_bomba, "timestamp": timestamp}',
         '{"mensaje": "Control de riego actualizado", '
         '"estado": estado_bomba, "timestamp": timestamp}'),
        
        ('SELECT temperatura, humedad, timestamp FROM registros_ambiente ORDER BY timestamp DESC LIMIT %s',
         'SELECT temperatura, humedad, timestamp FROM registros_ambiente '
         'ORDER BY timestamp DESC LIMIT %s'),
        
        ('INSERT INTO configuracion (temp_min, temp_max, hum_min, hum_max) VALUES (%s, %s, %s, %s)',
         'INSERT INTO configuracion (temp_min, temp_max, hum_min, hum_max) '
         'VALUES (%s, %s, %s, %s)'),
    ]
    
    for old_line, new_line in long_lines:
        content = content.replace(old_line, new_line)
    
    # Escribir archivo corregido
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Errores de linting corregidos")

if __name__ == '__main__':
    fix_app_py()