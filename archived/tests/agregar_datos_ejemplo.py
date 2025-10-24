#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agregar datos de ejemplo para mostrar en la interfaz
"""

import pymysql
from datetime import datetime, timedelta
import random

def agregar_datos_ejemplo():
    """Agregar varios registros de ejemplo"""
    try:
        conn = pymysql.connect(
            host='localhost', 
            user='root', 
            password='root', 
            database='invernadero'
        )
        
        cur = conn.cursor()
        
        # Agregar varios registros con diferentes tiempos
        now = datetime.now()
        
        registros = [
            (now - timedelta(hours=2), 23.5, 65.0, "Apagada", "Normal"),
            (now - timedelta(hours=1), 24.2, 68.5, "Encendida", "Normal"),
            (now - timedelta(minutes=30), 25.1, 70.2, "Encendida", "Normal"),
            (now - timedelta(minutes=15), 24.8, 67.8, "Encendida", "Normal"),
            (now - timedelta(minutes=5), 24.5, 66.5, "Apagada", "Normal"),
            (now, 24.3, 65.8, "Apagada", "Normal")
        ]
        
        for fecha, temp, hum, bomba, alerta in registros:
            cur.execute("""
                INSERT INTO registros_ambiente (fecha, temperatura, humedad, estado_bomba, alerta) 
                VALUES (%s, %s, %s, %s, %s)
            """, (fecha, temp, hum, bomba, alerta))
        
        conn.commit()
        print(f"✅ Se agregaron {len(registros)} registros de ejemplo")
        
        # Verificar datos
        cur.execute("SELECT COUNT(*) as total FROM registros_ambiente")
        total = cur.fetchone()[0]
        print(f"📊 Total de registros en BD: {total}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error agregando datos: {e}")
        return False

if __name__ == "__main__":
    agregar_datos_ejemplo()