# 📚 Manual de Instalación y Configuración
# Sistema de Invernadero Automatizado IoT

## 🎯 **Requisitos del Sistema**

### **Hardware Mínimo Requerido:**
- **Servidor/PC**: 2GB RAM, 10GB almacenamiento, Ubuntu 18.04+ / Windows 10+
- **Conectividad**: WiFi 2.4GHz con acceso a internet
- **Arduino/ESP32**: Ver lista detallada en `/arduino/README_ARDUINO.md`

### **Software Requerido:**
- Docker Desktop 20.10+
- Git 2.30+
- Arduino IDE 2.0+ (para programar microcontrolador)
- Navegador web moderno (Chrome, Firefox, Edge)

---

## 🚀 **Instalación Paso a Paso**

### **1. Preparación del Entorno**

```bash
# 1. Clonar el repositorio
git clone https://github.com/Yessi0908/Proyecto-de-arquitectura.git
cd Proyecto-de-arquitectura

# 2. Verificar Docker instalado
docker --version
docker-compose --version

# 3. Crear red de Docker (opcional)
docker network create invernadero-network
```

### **2. Configuración del Backend**

```bash
# Verificar estructura de archivos
ls -la
# Debe mostrar: docker-compose.yml, backend/, arduino/, docs/

# Construir e iniciar contenedores
docker-compose up --build -d

# Verificar que los servicios estén corriendo
docker-compose ps
```

**Salida esperada:**
```
NAME                     STATUS    PORTS
invernadero_backend      running   0.0.0.0:5000->5000/tcp
invernadero_db           running   0.0.0.0:3306->3306/tcp
```

### **3. Verificación de la Instalación**

```bash
# Probar conectividad a la API
curl http://localhost:5000/api/init -X POST -H "Content-Type: application/json" -d "{}"

# Acceder al dashboard web
# Abrir navegador en: http://localhost:5000
```

### **4. Configuración de Arduino/ESP32**

Ver documentación completa en: `/arduino/README_ARDUINO.md`

**Resumen rápido:**
1. Instalar librerías requeridas en Arduino IDE
2. Conectar sensores según diagrama de pines
3. Modificar variables WiFi y servidor en el código
4. Subir código al ESP32
5. Verificar comunicación en Monitor Serie

---

## ⚙️ **Configuración Avanzada**

### **Variables de Entorno**

Crear archivo `.env` en la raíz del proyecto:

```env
# Base de Datos
DB_HOST=db
DB_USER=root
DB_PASSWORD=tu_password_seguro
DB_NAME=invernadero

# Servidor Flask
FLASK_ENV=production
FLASK_DEBUG=False

# Puerto personalizado
BACKEND_PORT=5000
DB_PORT=3306

# Configuración de alertas (futuro)
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_USER=tu_email@gmail.com
EMAIL_PASSWORD=tu_password_app
```

**Luego modificar `docker-compose.yml`:**
```yaml
environment:
  - DB_HOST=${DB_HOST}
  - DB_USER=${DB_USER}
  - DB_PASSWORD=${DB_PASSWORD}
  - DB_NAME=${DB_NAME}
```

### **Configuración de Puertos**

Para cambiar puertos por defecto:

```yaml
# En docker-compose.yml
services:
  backend:
    ports:
      - "8080:5000"  # Cambiar puerto 5000 a 8080
  db:
    ports:
      - "3307:3306"  # Cambiar puerto MySQL a 3307
```

### **Volúmenes Persistentes**

Para conservar datos entre reinicios:

```yaml
volumes:
  db_data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: ./data/mysql  # Carpeta local para datos
```

---

## 🔧 **Configuración de Red y Firewall**

### **Puertos a Abrir:**

```bash
# Ubuntu/Linux
sudo ufw allow 5000/tcp  # Flask API
sudo ufw allow 3306/tcp  # MySQL (opcional, solo si acceso externo)

# Windows (PowerShell como administrador)
New-NetFirewallRule -DisplayName "Invernadero-API" -Direction Inbound -Port 5000 -Protocol TCP -Action Allow
```

### **Acceso desde Red Local:**

1. **Obtener IP del servidor:**
```bash
# Linux/Mac
ip addr show | grep inet
# Windows
ipconfig
```

2. **Modificar Arduino para usar IP real:**
```cpp
// En lugar de localhost, usar IP real del servidor
const char* serverURL = "http://192.168.1.100:5000";
```

3. **Acceder desde otros dispositivos:**
- Dashboard: `http://192.168.1.100:5000`
- Estadísticas: `http://192.168.1.100:5000/static/estadisticas.html`

---

## 📊 **Comandos de Administración**

### **Monitoreo del Sistema**

```bash
# Ver logs en tiempo real
docker-compose logs -f backend
docker-compose logs -f db

# Ver estado de contenedores
docker-compose ps

# Ver uso de recursos
docker stats

# Acceder a la base de datos
docker-compose exec db mysql -u root -p invernadero
```

### **Backup de Base de Datos**

```bash
# Crear backup
docker-compose exec db mysqldump -u root -p invernadero > backup_$(date +%Y%m%d_%H%M%S).sql

# Restaurar backup
docker-compose exec -T db mysql -u root -p invernadero < backup_20251020_143000.sql
```

### **Mantenimiento**

```bash
# Reiniciar servicios
docker-compose restart

# Actualizar código y reiniciar
git pull
docker-compose up --build -d

# Limpiar contenedores y volúmenes (¡CUIDADO: borra datos!)
docker-compose down -v
docker system prune -f
```

---

## 🛠️ **Solución de Problemas Comunes**

### **Error: Puerto 5000 ocupado**
```bash
# Verificar qué proceso usa el puerto
sudo lsof -i :5000
# Terminar proceso o cambiar puerto en docker-compose.yml
```

### **Error: No conecta a base de datos**
```bash
# Verificar que MySQL esté corriendo
docker-compose ps db
# Ver logs de MySQL
docker-compose logs db
# Reiniciar solo la base de datos
docker-compose restart db
```

### **Error: Arduino no envía datos**
1. Verificar conexión WiFi en Monitor Serie
2. Comprobar IP del servidor en código Arduino
3. Verificar firewall del servidor
4. Probar endpoint manualmente:
```bash
curl -X POST http://localhost:5000/api/sensores/ambiente \
  -H "Content-Type: application/json" \
  -d '{"temperatura":25.5,"humedad":60.2,"estado_bomba":"Apagada"}'
```

### **Dashboard no carga datos**
1. Abrir herramientas de desarrollador (F12)
2. Verificar errores en consola
3. Comprobar respuesta de API en pestaña Network
4. Verificar que backend esté corriendo: `curl http://localhost:5000/api/estado/actual`

---

## 🔐 **Seguridad y Mejores Prácticas**

### **Seguridad Básica:**
```bash
# Cambiar contraseñas por defecto
# Usar variables de entorno para credenciales
# Limitar acceso a puerto MySQL (solo localhost)
# Actualizar regularmente las imágenes Docker
```

### **Monitoreo de Logs:**
```bash
# Configurar rotación de logs
echo '{"log-driver": "json-file", "log-opts": {"max-size": "10m", "max-file": "3"}}' | sudo tee /etc/docker/daemon.json
sudo systemctl restart docker
```

### **SSL/HTTPS (Producción):**
Para usar en producción, configurar nginx con SSL:
```nginx
server {
    listen 443 ssl;
    server_name tu-dominio.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 🎯 **Pruebas del Sistema**

### **Test de Funcionalidad Básica:**
```bash
# 1. Test de API
curl http://localhost:5000/api/init -X POST

# 2. Test de inserción de datos
curl -X POST http://localhost:5000/api/sensores/ambiente \
  -H "Content-Type: application/json" \
  -d '{"temperatura":25,"humedad":60,"estado_bomba":"Apagada","alerta":"Normal"}'

# 3. Test de consulta
curl http://localhost:5000/api/estado/actual

# 4. Test de dashboard
curl http://localhost:5000/
```

### **Test de Arduino (Simulado):**
```bash
# Enviar datos de diferentes sensores
curl -X POST http://localhost:5000/api/sensores/seguridad \
  -H "Content-Type: application/json" \
  -d '{"tipo_evento":"Movimiento","descripcion":"Actividad en zona norte","nivel_alerta":"Medio"}'

curl -X POST http://localhost:5000/api/sensores/acceso \
  -H "Content-Type: application/json" \
  -d '{"id_tarjeta":"12345678","persona":"Admin","acceso_autorizado":true,"temperatura":24,"humedad":55}'
```

---

## 📈 **Escalabilidad y Mejoras Futuras**

### **Para entornos grandes:**
- Usar PostgreSQL en lugar de MySQL
- Implementar Redis para caché
- Configurar load balancer (nginx)
- Usar Kubernetes para orquestación

### **Funcionalidades adicionales:**
- Notificaciones por email/SMS
- App móvil nativa
- Integración con sistemas de riego avanzados
- Machine Learning para predicciones
- API REST con autenticación JWT

---

## 📞 **Soporte Técnico**

### **Logs importantes:**
```bash
# Logs del sistema completo
docker-compose logs --tail=100

# Solo errores
docker-compose logs backend | grep ERROR

# Base de datos
docker-compose logs db | tail -50
```

### **Información del sistema:**
```bash
# Versiones de software
docker --version
docker-compose --version
python --version

# Estado de contenedores
docker-compose ps
docker system df

# Conectividad
ping 8.8.8.8
curl -I http://localhost:5000
```

Para soporte adicional, revisar:
- Logs de contenedores
- Monitor Serie de Arduino
- Consola del navegador (F12)
- Issues en GitHub del proyecto