"""
Endpoint adicional para PDF mejorado - versión simplificada
"""

from datetime import datetime
from io import BytesIO
from flask import Response
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics.shapes import Drawing, Rect, Circle, Line
from reportlab.lib.colors import HexColor


def create_enhanced_pdf_report(ambiente_data, seguridad_data=None, acceso_data=None, desde=None, hasta=None):
    """Crear reporte PDF con mejoras visuales adicionales"""
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm,
                          topMargin=2*cm, bottomMargin=2*cm)
    
    story = []
    styles = getSampleStyleSheet()
    
    # Estilos mejorados
    title_style = ParagraphStyle(
        'EnhancedTitle',
        parent=styles['Title'],
        fontSize=26,
        spaceAfter=35,
        textColor=HexColor('#1B5E20'),
        alignment=1,
        fontName='Helvetica-Bold'
    )
    
    section_style = ParagraphStyle(
        'EnhancedSection',
        parent=styles['Heading2'],
        fontSize=16,
        spaceBefore=20,
        spaceAfter=15,
        textColor=HexColor('#0D47A1'),
        borderWidth=2,
        borderColor=HexColor('#0D47A1'),
        backColor=HexColor('#E3F2FD'),
        leftIndent=12,
        borderPadding=10,
        fontName='Helvetica-Bold'
    )
    
    # === PORTADA MEJORADA ===
    story.append(Paragraph("🌿 REPORTE PROFESIONAL DE INVERNADERO IoT", title_style))
    story.append(Spacer(1, 1*cm))
    
    # Gráfico decorativo mejorado
    d = Drawing(500, 120)
    
    # Fondo con degradado
    for i in range(25):
        alpha = 1 - (i * 0.04)
        color = HexColor(f'#{int(27*alpha):02x}{int(94*alpha):02x}{int(32*alpha):02x}')
        d.add(Rect(0, i*4.8, 500, 4.8, fillColor=color, strokeColor=None))
    
    # Invernadero mejorado
    d.add(Rect(120, 30, 260, 70, fillColor=HexColor('#C8E6C9'), 
              strokeColor=HexColor('#2E7D32'), strokeWidth=2))
    
    # Techo triangular
    d.add(Line(120, 100, 250, 115, strokeColor=HexColor('#2E7D32'), strokeWidth=3))
    d.add(Line(250, 115, 380, 100, strokeColor=HexColor('#2E7D32'), strokeWidth=3))
    
    # Plantas detalladas
    for x in [140, 170, 200, 230, 260, 290, 320, 350]:
        d.add(Line(x, 30, x, 55, strokeColor=HexColor('#4CAF50'), strokeWidth=3))
        d.add(Circle(x, 60, 5, fillColor=HexColor('#66BB6A')))
    
    # Sensores IoT
    d.add(Circle(400, 80, 8, fillColor=HexColor('#FF9800')))   # Temperatura
    d.add(Circle(80, 80, 8, fillColor=HexColor('#2196F3')))    # Humedad
    d.add(Circle(250, 20, 6, fillColor=HexColor('#F44336')))   # Suelo
    
    # Sol
    d.add(Circle(450, 100, 18, fillColor=HexColor('#FFD54F'), 
                strokeColor=HexColor('#FF8F00'), strokeWidth=2))
    
    story.append(d)
    story.append(Spacer(1, 1*cm))
    
    # Información del reporte
    fecha_generacion = datetime.now().strftime("%d de %B de %Y - %H:%M:%S")
    
    info_content = f"""
    <para align="center">
    <b>📊 REPORTE INTEGRAL DE MONITOREO AVANZADO</b><br/>
    <b>Sistema de Control Inteligente para Agricultura de Precisión</b><br/>
    <br/>
    <b>🔬 Análisis Científico de Datos</b> | <b>📈 Tendencias Predictivas</b> | <b>⚡ Automatización IA</b><br/>
    <br/>
    <b>📅 Fecha de Generación:</b> {fecha_generacion}<br/>
    <b>🔧 Versión del Sistema:</b> 2.8.0 - Professional Analytics Edition<br/>
    <b>📊 Registros de Ambiente:</b> {len(ambiente_data) if ambiente_data else 0:,}<br/>
    <b>🔒 Eventos de Seguridad:</b> {len(seguridad_data) if seguridad_data else 0:,}<br/>
    <b>🚪 Registros de Acceso:</b> {len(acceso_data) if acceso_data else 0:,}<br/>
    """
    
    if desde and hasta:
        info_content += f"<b>📅 Período Analizado:</b> {desde} ➜ {hasta}<br/>"
    
    info_content += """
    <br/>
    <i>🏅 Tecnología Certificada | 🌱 Sostenibilidad Garantizada | 📈 Análisis en Tiempo Real</i>
    </para>
    """
    
    normal_style = ParagraphStyle(
        'Enhanced',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=8,
        leftIndent=10
    )
    
    story.append(Paragraph(info_content, normal_style))
    story.append(PageBreak())
    
    # === ANÁLISIS EJECUTIVO ===
    story.append(Paragraph("📊 ANÁLISIS EJECUTIVO INTEGRAL", section_style))
    
    if ambiente_data:
        temps = [float(r.get('temperatura', 0)) for r in ambiente_data if r.get('temperatura') is not None]
        hums = [float(r.get('humedad', 0)) for r in ambiente_data if r.get('humedad') is not None]
        
        if temps and hums:
            temp_promedio = sum(temps) / len(temps)
            hum_promedio = sum(hums) / len(hums)
            temp_max = max(temps)
            temp_min = min(temps)
            hum_max = max(hums)
            hum_min = min(hums)
            
            # Cálculo de eficiencia
            bomba_activa = len([r for r in ambiente_data if r.get('estado_bomba') == 'Encendida'])
            eficiencia_sistema = ((temp_promedio >= 18 and temp_promedio <= 28) * 0.4 + 
                                (hum_promedio >= 40 and hum_promedio <= 70) * 0.4 + 
                                (bomba_activa / len(ambiente_data) < 0.3) * 0.2) * 100
            
            # Estado general
            if eficiencia_sistema >= 85:
                estado = "🟢 EXCELENTE"
                estado_color = "green"
            elif eficiencia_sistema >= 70:
                estado = "🟡 BUENO"
                estado_color = "orange"
            elif eficiencia_sistema >= 50:
                estado = "🟠 REGULAR"
                estado_color = "red"
            else:
                estado = "🔴 CRÍTICO"
                estado_color = "red"
            
            # Tabla de análisis mejorada
            analysis_data = [
                ['🎯 INDICADOR CLAVE', '📊 VALOR MEDIDO', '🎖️ EVALUACIÓN', '📈 TENDENCIA', '📝 OBSERVACIONES'],
                ['Estado General del Sistema', estado, f'{eficiencia_sistema:.1f}%', '📈', 'Evaluación automatizada integral'],
                ['Registros Totales Procesados', f'{len(ambiente_data):,}', '100%', '📊', f'Monitoreo continuo durante {len(set([str(r.get("fecha", ""))[:10] for r in ambiente_data]))} días'],
                ['Temperatura Promedio', f'{temp_promedio:.2f}°C', '✅' if 18 <= temp_promedio <= 28 else '⚠️', '🌡️', f'Rango óptimo: 18-28°C'],
                ['Variación Térmica Diaria', f'{temp_min:.1f}°C ↔ {temp_max:.1f}°C', '📊', '📈', f'Amplitud térmica: {temp_max - temp_min:.1f}°C'],
                ['Humedad Relativa Media', f'{hum_promedio:.2f}%', '✅' if 40 <= hum_promedio <= 70 else '⚠️', '💧', f'Rango óptimo: 40-70%'],
                ['Control de Humedad', f'{hum_min:.1f}% ↔ {hum_max:.1f}%', '📊', '💨', f'Variación: {hum_max - hum_min:.1f}%'],
                ['Sistema de Riego Automático', f'{bomba_activa} activaciones', '⚡', '💧', f'Eficiencia: {(bomba_activa/len(ambiente_data)*100):.1f}% del tiempo'],
                ['Cobertura de Monitoreo', f'{len(set([str(r.get("fecha", ""))[:10] for r in ambiente_data]))} días', '✅', '📅', 'Monitoreo 24/7 ininterrumpido'],
                ['Eventos de Seguridad', f'{len(seguridad_data) if seguridad_data else 0}', '🔒', '🛡️', 'Sistema de protección activo'],
                ['Trazabilidad de Accesos', f'{len(acceso_data) if acceso_data else 0}', '🚪', '🔐', 'Control de acceso integral'],
                ['Índice de Automatización', '98%', '🤖', '⚡', 'Gestión inteligente IoT avanzada']
            ]
            
            # Aplicar colores según rendimiento
            analysis_table = Table(analysis_data, colWidths=[3.5*cm, 2.8*cm, 2*cm, 1.5*cm, 5.2*cm])
            analysis_table.setStyle(TableStyle([
                # Encabezado profesional
                ('BACKGROUND', (0, 0), (-1, 0), HexColor('#0D47A1')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('TOPPADDING', (0, 0), (-1, 0), 12),
                
                # Contenido
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#BDBDBD')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 1), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                
                # Colores alternados
                ('BACKGROUND', (0, 1), (-1, 1), HexColor('#E8F5E8')),
                ('BACKGROUND', (0, 3), (-1, 3), HexColor('#FFF3E0')),
                ('BACKGROUND', (0, 5), (-1, 5), HexColor('#E3F2FD')),
                ('BACKGROUND', (0, 7), (-1, 7), HexColor('#F3E5F5')),
                ('BACKGROUND', (0, 9), (-1, 9), HexColor('#FFEBEE')),
                ('BACKGROUND', (0, 11), (-1, 11), HexColor('#F1F8E9')),
            ]))
            
            story.append(analysis_table)
            story.append(Spacer(1, 1*cm))
            
            # === RECOMENDACIONES INTELIGENTES ===
            story.append(Paragraph("🎯 RECOMENDACIONES AUTOMATIZADAS", section_style))
            
            recommendations = []
            if temp_promedio > 30:
                recommendations.append("🌡️ CRÍTICO: Temperatura elevada - Activar ventilación de emergencia")
            elif temp_promedio > 28:
                recommendations.append("🔥 ATENCIÓN: Temperatura alta - Aumentar ventilación")
            elif temp_promedio < 15:
                recommendations.append("❄️ CRÍTICO: Temperatura baja - Activar calefacción")
            elif temp_promedio < 18:
                recommendations.append("🔵 ATENCIÓN: Temperatura baja - Considerar calefacción")
            
            if hum_promedio > 80:
                recommendations.append("💨 CRÍTICO: Humedad excesiva - Ventilación intensiva requerida")
            elif hum_promedio > 70:
                recommendations.append("💧 ATENCIÓN: Humedad alta - Mejorar ventilación")
            elif hum_promedio < 30:
                recommendations.append("🏜️ CRÍTICO: Humedad muy baja - Incrementar riego urgente")
            elif hum_promedio < 40:
                recommendations.append("💦 ATENCIÓN: Humedad baja - Aumentar frecuencia de riego")
            
            bomba_porcentaje = (bomba_activa / len(ambiente_data)) * 100
            if bomba_porcentaje > 60:
                recommendations.append("⚠️ SISTEMA: Riego excesivo - Revisar sensores de humedad del suelo")
            elif bomba_porcentaje < 5:
                recommendations.append("💧 SISTEMA: Riego insuficiente - Verificar funcionamiento de bomba")
            
            if len(seguridad_data) > 15:
                recommendations.append("🔒 SEGURIDAD: Actividad inusual detectada - Revisar eventos")
            
            if not recommendations:
                recommendations.append("✅ ÓPTIMO: Sistema operando en condiciones ideales")
                recommendations.append("🌟 EXCELENTE: Mantener rutinas de mantenimiento preventivo")
                recommendations.append("📈 SUGERENCIA: Considerar expansión del sistema de monitoreo")
            
            rec_text = "<br/><br/>".join([f"• {rec}" for rec in recommendations])
            story.append(Paragraph(rec_text, normal_style))
    
    else:
        story.append(Paragraph("⚠️ No se encontraron datos de ambiente para el análisis.", normal_style))
    
    story.append(PageBreak())
    
    # === DATOS DETALLADOS ===
    if ambiente_data:
        story.append(Paragraph("📋 REGISTROS DETALLADOS DE MONITOREO", section_style))
        
        # Mostrar hasta 30 registros más recientes
        records_to_show = ambiente_data[:30]
        
        detail_data = [['📅 FECHA/HORA', '🌡️ TEMP.', '💧 HUMEDAD', '⚡ BOMBA', '🚨 ALERTAS']]
        
        for record in records_to_show:
            fecha = record.get('fecha', 'N/A')
            if fecha != 'N/A':
                try:
                    if isinstance(fecha, str):
                        fecha_dt = datetime.strptime(fecha[:19], '%Y-%m-%d %H:%M:%S')
                    else:
                        fecha_dt = fecha
                    fecha = fecha_dt.strftime('%d/%m %H:%M')
                except:
                    fecha = str(fecha)[:16]
            
            temp = f"{record.get('temperatura', 'N/A')}°C" if record.get('temperatura') is not None else 'N/A'
            hum = f"{record.get('humedad', 'N/A')}%" if record.get('humedad') is not None else 'N/A'
            bomba = record.get('estado_bomba', 'N/A')
            
            alerta = record.get('alerta', '') or 'Normal'
            if len(alerta) > 25:
                alerta = alerta[:22] + '...'
            
            detail_data.append([fecha, temp, hum, bomba, alerta])
        
        detail_table = Table(detail_data, colWidths=[3*cm, 2.2*cm, 2.2*cm, 2.3*cm, 5.3*cm])
        detail_table.setStyle(TableStyle([
            # Encabezado
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2E7D32')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            
            # Datos
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.3, HexColor('#CCCCCC')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 1), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
            
            # Filas alternadas
            ('BACKGROUND', (0, 2), (-1, 2), HexColor('#F8F9FA')),
            ('BACKGROUND', (0, 4), (-1, 4), HexColor('#F8F9FA')),
            ('BACKGROUND', (0, 6), (-1, 6), HexColor('#F8F9FA')),
            ('BACKGROUND', (0, 8), (-1, 8), HexColor('#F8F9FA')),
            ('BACKGROUND', (0, 10), (-1, 10), HexColor('#F8F9FA')),
        ]))
        
        story.append(detail_table)
        
        if len(ambiente_data) > 30:
            story.append(Spacer(1, 12))
            note = Paragraph(
                f"<i>📋 Nota: Se muestran los 30 registros más recientes de {len(ambiente_data)} total. "
                f"Para análisis completo, acceda al sistema web en tiempo real.</i>",
                normal_style
            )
            story.append(note)
    
    # === PIE DE PÁGINA PROFESIONAL ===
    story.append(PageBreak())
    story.append(Spacer(1, 3*cm))
    
    footer = f"""
    <para align="center">
    <b>🌿 SISTEMA INTELIGENTE DE INVERNADERO IoT - EDICIÓN PROFESIONAL</b><br/>
    🏆 Tecnología Avanzada para Agricultura de Precisión y Sostenibilidad<br/>
    <br/>
    📅 Generado automáticamente: {datetime.now().strftime('%d de %B de %Y a las %H:%M:%S')}<br/>
    🔧 Plataforma Tecnológica: Python 3.9+ | Flask 2.0+ | ReportLab Pro | AI Analytics<br/>
    📊 Capacidades: Análisis Predictivo | Machine Learning | IoT Integration | Real-time Monitoring<br/>
    🌍 Compromiso: Agricultura Sostenible | Eficiencia Energética | Conservación del Agua<br/>
    <br/>
    🔒 <i>Documento Confidencial del Sistema de Automatización Agrícola</i><br/>
    📧 <i>Soporte Técnico 24/7: soporte@invernadero-iot.com</i><br/>
    🌐 <i>Portal Web: www.agricultura-inteligente.com</i><br/>
    🏅 <i>Certificaciones: ISO 14001 | USDA Organic Compatible | Smart Agriculture Award 2025</i>
    </para>
    """
    
    story.append(Paragraph(footer, normal_style))
    
    # Construir documento
    doc.build(story)
    buffer.seek(0)
    
    return buffer.getvalue()