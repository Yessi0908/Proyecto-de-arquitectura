# Test simple de PDF con ReportLab - VERSIÓN MEJORADA
from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.graphics.shapes import Drawing, Rect, Circle, Line

def crear_pdf_mejorado():
    """Crear PDF mejorado de prueba con todos los elementos visuales"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm,
                          topMargin=2*cm, bottomMargin=2*cm)
    
    story = []
    styles = getSampleStyleSheet()
    
    # Estilo personalizado para título
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=24,
        spaceAfter=30,
        textColor=HexColor('#2E7D32'),
        alignment=1
    )
    
    # Título principal
    titulo = Paragraph("🌿 REPORTE INVERNADERO IoT - PRUEBA MEJORADA", title_style)
    story.append(titulo)
    story.append(Spacer(1, 1*cm))
    
    # Gráfico decorativo simple
    d = Drawing(400, 100)
    
    # Fondo
    d.add(Rect(0, 0, 400, 100, fillColor=HexColor('#E8F5E8'), strokeColor=HexColor('#4CAF50')))
    
    # Invernadero simple
    d.add(Rect(50, 20, 150, 60, fillColor=HexColor('#C8E6C9'), strokeColor=HexColor('#2E7D32')))
    d.add(Line(125, 80, 100, 90, strokeColor=HexColor('#2E7D32'), strokeWidth=2))
    d.add(Line(125, 80, 150, 90, strokeColor=HexColor('#2E7D32'), strokeWidth=2))
    
    # Plantas
    for x in [70, 90, 110, 130, 150, 170]:
        d.add(Line(x, 20, x, 40, strokeColor=HexColor('#4CAF50'), strokeWidth=2))
        d.add(Circle(x, 42, 3, fillColor=HexColor('#66BB6A')))
    
    # Sol
    d.add(Circle(350, 80, 15, fillColor=HexColor('#FFD54F')))
    
    # Sensores
    d.add(Circle(300, 50, 5, fillColor=HexColor('#FF9800')))  # Temperatura
    d.add(Circle(320, 30, 5, fillColor=HexColor('#2196F3')))  # Humedad
    
    story.append(d)
    story.append(Spacer(1, 1*cm))
    
    # Información del sistema
    info = f"""
    <para align="center">
    <b>📊 SISTEMA DE MONITOREO AVANZADO</b><br/>
    <br/>
    <b>Fecha de Generación:</b> {datetime.now().strftime('%d de %B de %Y - %H:%M:%S')}<br/>
    <b>Versión:</b> 2.5.0 - Professional Edition<br/>
    <b>Estado:</b> 🟢 Operativo<br/>
    <b>Características:</b> Gráficos | Análisis | Automatización<br/>
    </para>
    """
    
    story.append(Paragraph(info, styles['Normal']))
    story.append(Spacer(1, 1*cm))
    
    # Tabla de datos de prueba
    data = [
        ['🎯 MÉTRICA', '📊 VALOR', '🎖️ ESTADO', '📝 OBSERVACIONES'],
        ['Temperatura', '25.5°C', '✅ Óptimo', 'Rango ideal para cultivo'],
        ['Humedad', '65.2%', '✅ Óptimo', 'Condiciones perfectas'],
        ['Sistema Riego', 'Automático', '⚡ Activo', 'Funcionamiento normal'],
        ['Sensores', '4 Activos', '🔍 Monitoreando', 'Todos operativos'],
        ['Conectividad', 'WiFi + LoRa', '📶 Excelente', 'Red estable'],
        ['Análisis IA', 'Habilitado', '🤖 Procesando', 'Predicciones activas']
    ]
    
    tabla = Table(data, colWidths=[3*cm, 2.5*cm, 2.5*cm, 7*cm])
    tabla.setStyle(TableStyle([
        # Encabezado
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1565C0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        
        # Datos
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#CCCCCC')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        
        # Colores alternados
        ('BACKGROUND', (0, 1), (-1, 1), HexColor('#E8F5E8')),
        ('BACKGROUND', (0, 3), (-1, 3), HexColor('#FFF3E0')),
        ('BACKGROUND', (0, 5), (-1, 5), HexColor('#E3F2FD')),
    ]))
    
    story.append(tabla)
    story.append(Spacer(1, 1*cm))
    
    # Recomendaciones
    section_style = ParagraphStyle(
        'SectionStyle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceBefore=15,
        spaceAfter=10,
        textColor=HexColor('#1565C0'),
        borderWidth=1,
        borderColor=HexColor('#1565C0'),
        backColor=HexColor('#E3F2FD'),
        leftIndent=10,
        borderPadding=8
    )
    
    story.append(Paragraph("🎯 RECOMENDACIONES AUTOMATIZADAS", section_style))
    
    recomendaciones = """
    • ✅ <b>Sistema Óptimo:</b> Todas las condiciones dentro de rangos ideales<br/>
    • 📈 <b>Mantenimiento:</b> Calibración de sensores programada para próxima semana<br/>
    • 🌱 <b>Cultivo:</b> Condiciones perfectas para siembra de temporada<br/>
    • 💧 <b>Riego:</b> Eficiencia del 95% - Sistema funcionando correctamente<br/>
    • 🔋 <b>Energía:</b> Consumo optimizado - Paneles solares cubriendo 80%<br/>
    • 📊 <b>Datos:</b> Recolección continua - Base de datos actualizada<br/>
    """
    
    story.append(Paragraph(recomendaciones, styles['Normal']))
    story.append(Spacer(1, 2*cm))
    
    # Pie de página
    footer = f"""
    <para align="center">
    <b>🌿 Sistema Inteligente de Invernadero IoT</b><br/>
    Tecnología Avanzada para Agricultura de Precisión<br/>
    <br/>
    📧 Soporte: admin@invernadero-iot.com | 🌐 www.agricultura-inteligente.com<br/>
    🔒 Documento generado automáticamente - Confidencial
    </para>
    """
    
    story.append(Paragraph(footer, styles['Normal']))
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

if __name__ == '__main__':
    try:
        print("🔄 Generando PDF mejorado de prueba...")
        pdf_data = crear_pdf_mejorado()
        
        with open('reporte_mejorado_prueba.pdf', 'wb') as f:
            f.write(pdf_data)
        
        print(f"✅ PDF mejorado creado exitosamente: {len(pdf_data):,} bytes")
        print("📄 Archivo guardado como: reporte_mejorado_prueba.pdf")
        
        # Verificar características
        print("\n📊 Características del PDF generado:")
        print("   • ✅ Gráficos vectoriales")
        print("   • ✅ Tablas profesionales")
        print("   • ✅ Colores personalizados")
        print("   • ✅ Estilos avanzados")
        print("   • ✅ Diseño responsivo")
        print("   • ✅ Información detallada")
        
    except Exception as e:
        print(f"❌ Error generando PDF: {e}")
        import traceback
        traceback.print_exc()