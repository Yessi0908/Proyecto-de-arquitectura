#!/usr/bin/env python3
"""
Script para crear la base de datos e insertar datos de prueba
"""

import pymysql
import os
from datetime import datetime

# Configuración de base de datos
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'root'
DB_NAME = 'invernadero'

def create_database_and_data():
    """Crear base de datos e insertar datos de prueba"""
    
    print("🔄 Conectando a MySQL...")
    
    try:
        # Conectar sin especificar base de datos para crearla
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            charset='utf8mb4'
        )
        
        with conn.cursor() as cursor:
            # Crear base de datos
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
            print(f"✅ Base de datos '{DB_NAME}' creada/verificada")
        
        conn.close()
        
        # Conectar a la base de datos específica
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset='utf8mb4'
        )
        
        with conn.cursor() as cursor:
            # Crear tabla de registros de ambiente
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS registros_ambiente (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
                    temperatura FLOAT,
                    humedad FLOAT,
                    estado_bomba VARCHAR(15),
                    alerta VARCHAR(50)
                )
            ''')
            print("✅ Tabla 'registros_ambiente' creada/verificada")
            
            # Crear tabla de seguridad
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS registros_seguridad (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
                    tipo_evento VARCHAR(20),
                    descripcion TEXT,
                    nivel_alerta VARCHAR(15)
                )
            ''')
            print("✅ Tabla 'registros_seguridad' creada/verificada")
            
            # Crear tabla de accesos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS registros_acceso (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
                    persona VARCHAR(50),
                    acceso_autorizado BOOLEAN
                )
            ''')
            print("✅ Tabla 'registros_acceso' creada/verificada")
            
            # Crear tabla de configuración
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS config_umbrales (
                    id INT PRIMARY KEY DEFAULT 1,
                    humo_umbral INT DEFAULT 300,
                    humo_critico INT DEFAULT 500
                )
            ''')
            print("✅ Tabla 'config_umbrales' creada/verificada")
            
            # Insertar datos de prueba para ambiente
            datos_ambiente = [
                (25.5, 65.0, 'Apagada', 'Normal'),
                (27.2, 58.0, 'Apagada', 'Normal'),
                (23.8, 72.0, 'Encendida', 'Medio'),
                (26.1, 62.0, 'Apagada', 'Normal'),
                (24.7, 68.0, 'Apagada', 'Normal'),
                (28.3, 55.0, 'Apagada', 'Normal'),
                (22.9, 75.0, 'Encendida', 'Alto'),
                (25.8, 63.0, 'Apagada', 'Normal')
            ]
            
            # Limpiar datos existentes
            cursor.execute("DELETE FROM registros_ambiente")
            
            for temp, hum, bomba, alerta in datos_ambiente:
                cursor.execute('''
                    INSERT INTO registros_ambiente (temperatura, humedad, estado_bomba, alerta)
                    VALUES (%s, %s, %s, %s)
                ''', (temp, hum, bomba, alerta))
            
            print(f"✅ {len(datos_ambiente)} registros de ambiente insertados")
            
            # Insertar datos de seguridad
            cursor.execute("DELETE FROM registros_seguridad")
            cursor.execute('''
                INSERT INTO registros_seguridad (tipo_evento, descripcion, nivel_alerta)
                VALUES ('Movimiento', 'Movimiento detectado en zona norte', 'Medio')
            ''')
            print("✅ Registros de seguridad insertados")
            
            # Insertar datos de acceso
            cursor.execute("DELETE FROM registros_acceso")
            cursor.execute('''
                INSERT INTO registros_acceso (persona, acceso_autorizado)
                VALUES ('Juan Pérez', TRUE)
            ''')
            print("✅ Registros de acceso insertados")
            
            # Insertar configuración por defecto
            cursor.execute('''
                INSERT INTO config_umbrales (id, humo_umbral, humo_critico)
                VALUES (1, 300, 500)
                ON DUPLICATE KEY UPDATE
                humo_umbral = VALUES(humo_umbral),
                humo_critico = VALUES(humo_critico)
            ''')
            print("✅ Configuración de umbrales insertada")
            
            # Confirmar cambios
            conn.commit()
            
            # Verificar los datos insertados
            cursor.execute("SELECT COUNT(*) FROM registros_ambiente")
            count = cursor.fetchone()[0]
            print(f"📊 Total de registros en base de datos: {count}")
            
            # Mostrar algunos registros
            cursor.execute("SELECT * FROM registros_ambiente ORDER BY fecha DESC LIMIT 3")
            registros = cursor.fetchall()
            print("🔍 Últimos registros:")
            for reg in registros:
                print(f"   ID: {reg[0]}, Fecha: {reg[1]}, Temp: {reg[2]}°C, Hum: {reg[3]}%")
        
        conn.close()
        print("✅ Base de datos configurada correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error configurando base de datos: {e}")
        return False

if __name__ == '__main__':
    if create_database_and_data():
        print("\n🎉 ¡Base de datos lista!")
        print("📊 Ahora puedes iniciar el servidor Flask original:")
        print("   python backend/app.py")
    else:
        print("\n❌ Falló la configuración de la base de datos")
        print("🔧 Verifica que MySQL esté ejecutándose y las credenciales sean correctas")