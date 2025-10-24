# 📖 Manual de Usuario
# Sistema de Invernadero Automatizado IoT

## 🌿 **Bienvenido al Sistema de Invernadero Inteligente**

Este manual te guiará a través de todas las funcionalidades del sistema de monitoreo y automatización de tu invernadero.

---

## 🏠 **Dashboard Principal**

### **Acceso al Sistema:**
1. Abrir navegador web
2. Ir a: `http://[IP-DEL-SERVIDOR]:5000`
3. La página se carga automáticamente

### **Vista General del Dashboard:**

#### **📊 Panel de Estado (Tarjetas Superiores):**

**🌡️ Tarjeta de Ambiente:**
- **Temperatura actual**: Color verde (normal), amarillo (advertencia), rojo (crítico)
- **Humedad actual**: Porcentaje con indicación visual
- **Estado de bomba**: "Encendida" o "Apagada" con color indicativo

**🚨 Tarjeta de Seguridad:**
- **Movimiento**: "Detectado" o "No detectado"
- **Humo**: Estado del sensor de humo
- **Alerta general**: Nivel de alerta con emoticón de color

**🪪 Tarjeta de Control de Acceso:**
- **Último acceso**: Hora del último acceso registrado
- **Usuario**: Nombre de la persona que accedió
- **Estado**: "Autorizado ✅" o "No Autorizado ❌"

#### **📈 Gráfico de Tendencias:**
- Muestra histórico de temperatura y humedad
- Se actualiza automáticamente con datos reales
- Líneas de colores: Roja (temperatura), Azul (humedad)

#### **🧾 Historial de Eventos:**
- Lista de eventos recientes del sistema
- Columnas: Fecha/Hora, Evento, Descripción, Nivel de alerta
- Colores: Verde (normal), Amarillo (advertencia), Rojo (crítico)

### **🔧 Controles del Dashboard:**

**Filtros Avanzados:**
- **Fecha Desde/Hasta**: Filtrar eventos por rango de fechas
- **Tipo de Evento**: Filtrar por Ambiente, Movimiento, Humo, Acceso
- **Nivel de Alerta**: Filtrar por Normal, Medio, Alto, Crítico

**Botones de Control:**
- **🔄 Refrescar datos**: Actualización manual inmediata
- **🔍 Aplicar Filtros**: Aplicar filtros seleccionados
- **📊 Estadísticas**: Ir a página de estadísticas avanzadas
- **📄 Descargar PDF**: Generar reporte en PDF
- **⏸️ Pausar Auto-actualización**: Pausar/reanudar actualizaciones automáticas

### **⚡ Actualizaciones Automáticas:**
- El dashboard se actualiza cada 10 segundos automáticamente
- Los colores cambian según los valores y umbrales configurados
- Las alertas aparecen instantáneamente cuando ocurren eventos

---

## 📊 **Página de Estadísticas**

### **Acceso:**
Hacer clic en el botón "📊 Estadísticas" desde el dashboard principal.

### **Funcionalidades:**

#### **⚠️ Alertas del Sistema:**
- **Panel superior**: Muestra alertas activas en tiempo real
- **Colores**: Rojo (crítico), Amarillo (alto), Azul (información)
- **Información**: Tipo de alerta, mensaje descriptivo, fecha/hora

#### **📈 Resumen General:**
**Tarjetas de métricas:**
- **Registros Ambientales**: Total de lecturas de sensores
- **Eventos de Seguridad**: Total de detecciones de seguridad
- **Accesos Registrados**: Total de intentos de acceso RFID
- **Activaciones de Bomba**: Veces que se activó el riego automático

#### **📊 Estadísticas Detalladas:**

**🌡️ Condiciones Ambientales:**
- **Temperatura**: Promedio, mínima y máxima del período
- **Humedad**: Promedio, mínima y máxima del período
- Valores con colores indicativos según rangos

**🚨 Eventos de Seguridad:**
- **Contadores**: Movimiento, humo, alertas críticas y altas
- **Barra de seguridad**: Nivel general de seguridad del sistema
- Verde (>80% seguro), Amarillo (60-80%), Rojo (<60%)

**🪪 Control de Acceso:**
- **Autorizados vs Denegados**: Conteo de accesos por tipo
- **Tasa de autorización**: Porcentaje de accesos válidos
- **Barra de progreso**: Verde (>90%), Amarillo (70-90%), Rojo (<70%)

#### **📊 Gráficos Interactivos:**
- **Tendencia de Temperatura**: Gráfico de líneas semanal
- **Tendencia de Humedad**: Gráfico de líneas semanal
- **Distribución de Alertas**: Gráfico de dona con porcentajes
- **Resumen Semanal**: Métricas de eficiencia del sistema

### **⚙️ Configuración de Umbrales:**

**Cómo configurar alertas personalizadas:**

1. **🌡️ Temperatura (°C):**
   - **Mín**: Temperatura mínima aceptable (ej: 18°C)
   - **Máx**: Temperatura máxima aceptable (ej: 28°C) 
   - **Crítica**: Temperatura de emergencia (ej: 35°C)

2. **💧 Humedad (%):**
   - **Mín**: Humedad mínima aceptable (ej: 40%)
   - **Máx**: Humedad máxima aceptable (ej: 70%)

3. **💨 Humo:**
   - **Umbral**: Nivel de detección (ej: 300)
   - **Crítico**: Nivel de emergencia (ej: 500)

4. **Guardar**: Hacer clic en "💾 Guardar Configuración"

**Efectos de los umbrales:**
- **Sistema de riego**: Se activa automáticamente si temperatura/humedad salen del rango
- **Alertas visuales**: Cambio de colores en dashboard
- **Registros**: Se almacenan eventos cuando se superan umbrales

---

## 🎛️ **Sistema de Control Automático**

### **Control de Riego:**

**La bomba se ENCIENDE automáticamente cuando:**
- Temperatura > Máxima configurada (defecto: 28°C)
- Humedad < Mínima configurada (defecto: 40%)

**La bomba se APAGA automáticamente cuando:**
- Temperatura vuelve al rango normal
- Humedad vuelve al rango normal

**Indicadores visuales:**
- **Verde**: Bomba apagada, condiciones normales
- **Amarillo**: Bomba encendida, corrigiendo condiciones

### **Sistema de Alertas:**

**🟢 Estado Normal:**
- Temperatura 18-28°C
- Humedad 40-70%
- Sin humo detectado
- Sin movimiento inusual

**🟡 Advertencia:**
- Temperatura 15-18°C o 28-32°C
- Humedad 30-40% o 70-80%
- Humo bajo detectado
- Movimiento normal

**🔴 Alerta Crítica:**
- Temperatura <15°C o >35°C
- Humedad <30% o >80%
- Humo alto detectado
- Acceso no autorizado

---

## 🪪 **Control de Acceso RFID**

### **Cómo usar el sistema de acceso:**

1. **Acercar tarjeta RFID** al lector (distancia < 3cm)
2. **Esperar confirmación:**
   - **✅ Acceso Autorizado**: LED verde + 1 beep largo
   - **❌ Acceso Denegado**: LED rojo + 5 beeps cortos

### **Información registrada en cada acceso:**
- ID de la tarjeta utilizada
- Nombre del usuario (si está registrado)
- Fecha y hora exacta del acceso
- Estado del sistema (temperatura, humedad, bomba)
- Estado de autorización (autorizado/denegado)

### **Ver historial de accesos:**
1. Ir al dashboard principal
2. En "Historial de eventos" aparecen los accesos
3. O usar filtros: Tipo de Evento → "Acceso"

---

## 📄 **Generación de Reportes**

### **Reporte PDF Básico:**
1. Hacer clic en "📄 Descargar PDF" en el dashboard
2. Se genera automáticamente con datos de ambiente
3. Incluye registros de temperatura, humedad y estado de bomba

### **Reportes Filtrados:**
1. Configurar filtros de fecha en el dashboard
2. Aplicar filtros
3. Descargar PDF con datos filtrados

### **Contenido de los reportes:**
- Encabezado con título del invernadero
- Lista de registros ambientales con timestamps
- Formato: Fecha | Temperatura | Humedad | Estado Bomba

---

## 🚨 **Qué Hacer en Casos de Emergencia**

### **🔴 Alerta de Temperatura Crítica:**
1. **Verificar**: ¿El sistema activó la bomba automáticamente?
2. **Acciones manuales**: 
   - Abrir ventilación manual si existe
   - Verificar que la bomba tenga agua
   - Revisar sensor por posible fallo
3. **Monitorear**: Esperar 10-15 minutos para normalización

### **🔴 Detección de Humo:**
1. **Seguridad primero**: Evaluar riesgo de incendio
2. **Acciones inmediatas**:
   - Verificar fuentes de calor en el invernadero
   - Revisar conexiones eléctricas
   - Ventilar el área si es seguro
3. **Sistema**: La alerta se registra automáticamente

### **🔴 Acceso No Autorizado:**
1. **Verificar**: Revisar historial de accesos en tiempo real
2. **Investigar**: ¿Quién intentó acceder?
3. **Seguridad**: Considerar cambiar tarjetas si es necesario
4. **Sistema**: Todos los intentos se registran con timestamp

### **🔴 Pérdida de Conexión:**
Si el dashboard no actualiza:
1. **Verificar WiFi** del Arduino/ESP32
2. **Revisar servidor**: ¿Está el sistema backend funcionando?
3. **Red local**: ¿Hay conectividad en la red?
4. **Contactar administrador** si persiste el problema

---

## 💡 **Consejos de Uso Óptimo**

### **Monitoreo Diario:**
- Revisar dashboard al menos 2 veces al día
- Verificar que las alertas estén en verde
- Comprobar que los datos se actualizan (timestamp reciente)

### **Mantenimiento Semanal:**
- Revisar estadísticas semanales
- Verificar eficiencia del sistema de riego
- Limpiar sensor de humo si es necesario
- Comprobar baterías de sensores inalámbricos

### **Configuración Estacional:**
- **Verano**: Reducir umbrales de temperatura máxima
- **Invierno**: Aumentar umbrales de temperatura mínima  
- **Lluvias**: Ajustar umbrales de humedad máxima
- **Sequía**: Reducir umbrales de humedad mínima

### **Optimización de Riego:**
- Observar patrones de activación de bomba
- Ajustar umbrales si hay demasiadas/pocas activaciones
- Considerar horarios de riego (early morning/evening)

---

## ❓ **Preguntas Frecuentes**

### **¿Por qué el dashboard no actualiza los datos?**
- Verificar conexión de internet
- Comprobar que el ESP32 esté conectado a WiFi
- Revisar LED de estado en el hardware

### **¿Cómo sé si la bomba está funcionando correctamente?**
- Verificar en dashboard: Estado bomba = "Encendida"
- Escuchar sonido de la bomba física
- Comprobar flujo de agua en sistema de riego

### **¿Por qué hay muchas alertas de movimiento?**
- Puede ser sensibilidad alta del sensor PIR
- Animales pequeños o viento fuerte
- Revisar ubicación del sensor

### **¿Qué hago si pierdo una tarjeta RFID?**
- Reportar al administrador del sistema
- Solicitar nueva tarjeta programada
- Cambiar configuración en código Arduino si es necesario

### **¿Cómo cambio los horarios de riego?**
- Actualmente el sistema es reactivo (responde a condiciones)
- Para horarios programados, contactar al desarrollador
- Se puede implementar funcionalidad adicional

---

## 📞 **Contacto y Soporte**

### **Para soporte técnico:**
- Revisar documentación en `/docs/INSTALACION.md`
- Verificar logs del sistema
- Contactar administrador de TI

### **Para modificaciones del sistema:**
- Solicitar cambios al equipo de desarrollo
- Proporcionar detalles específicos de la necesidad
- Considerar impacto en funcionalidades existentes

### **Reportar problemas:**
1. Anotar fecha y hora del problema
2. Hacer captura de pantalla del error
3. Describir pasos que causaron el problema
4. Incluir información de navegador/dispositivo usado

---

**¡Gracias por usar nuestro Sistema de Invernadero Automatizado! 🌱**

*Para obtener mejores resultados, familiarízate con todas las funcionalidades y revisa regularmente el estado del sistema.*