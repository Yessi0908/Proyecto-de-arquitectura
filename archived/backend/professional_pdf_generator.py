"""
Generador de PDF profesional que replica el diseño específico mostrado
Sistema de Invernadero IoT - Formato de producción
"""

from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas


class ProductionPDFGenerator:
    """Generador de PDF que replica exactamente el diseño de producción"""
    
    def __init__(self):
        self.page_width, self.page_height = A4
        self.margin = 2*cm
        
        # Colores exactos del diseño
        self.colors = {
            'header_green': HexColor('#2E7D32'),      # Verde del encabezado
            'section_blue': HexColor('#1976D2'),      # Azul de secciones
            'table_gray': HexColor('#F5F5F5'),        # Gris claro de tabla
            'border_gray': HexColor('#E0E0E0'),       # Gris de bordes
            'text_black': colors.black,
            'white': colors.white,
            'red_alert': HexColor('#F44336'),         # Rojo para alertas
            'green_ok': HexColor('#4CAF50'),          # Verde para OK
            'orange_warning': HexColor('#FF9800'),     # Naranja para advertencias
        }
        
        self.setup_styles()
    
    def setup_styles(self):
        """Configurar estilos específicos del diseño"""
        self.styles = getSampleStyleSheet()
        
        # Título principal (verde)
        self.styles.add(ParagraphStyle(
            name='MainTitle',
            parent=self.styles['Title'],
            fontSize=18,
            textColor=self.colors['white'],
            alignment=0,  # Izquierda
            fontName='Helvetica-Bold',
            spaceAfter=0,
            spaceBefore=0
        ))
        
        # Información del sistema
        self.styles.add(ParagraphStyle(
            name='SystemInfo',
            fontSize=9,
            textColor=self.colors['white'],
            alignment=0,
            fontName='Helvetica',
            spaceAfter=0,
            spaceBefore=0
        ))
        
        # Título de sección azul
        self.styles.add(ParagraphStyle(
            name='SectionTitle',
            fontSize=14,
            textColor=self.colors['white'],
            alignment=0,
            fontName='Helvetica-Bold',
            spaceAfter=0,
            spaceBefore=10
        ))
        
        # Texto normal
        self.styles.add(ParagraphStyle(
            name='Normal',
            fontSize=10,
            textColor=self.colors['text_black'],
            alignment=0,
            fontName='Helvetica'
        ))

    def draw_header_box(self, canvas, x, y, width, height, color, text, style='MainTitle'):
        """Dibujar caja de encabezado con color de fondo"""
        canvas.setFillColor(color)
        canvas.setStrokeColor(color)
        canvas.rect(x, y, width, height, fill=1)
        
        # Añadir texto sobre la caja
        text_obj = canvas.beginText(x + 10, y + height/2 - 5)
        text_obj.setFont("Helvetica-Bold", 18 if style == 'MainTitle' else 14)
        text_obj.setFillColor(self.colors['white'])
        text_obj.textLine(text)
        canvas.drawText(text_obj)

    def create_summary_table(self, ambiente_data):
        """Crear tabla de resumen ejecutivo exactamente como en la imagen"""
        if not ambiente_data:
            # Tabla vacía si no hay datos
            data = [
                ['Métrica', 'Valor', 'Unidad'],
                ['Total de Registros', '0', 'registros'],
                ['Temperatura Promedio', '0.0', '°C'],
                ['Temperatura Máxima', '0.0', '°C'],
                ['Temperatura Mínima', '0.0', '°C'],
                ['Humedad Promedio', '0.0', '%'],
                ['Humedad Máxima', '0.0', '%'],
                ['Humedad Mínima', '0.0', '%'],
                ['Activaciones de Riego', '0', 'veces'],
            ]
        else:
            # Calcular estadísticas
            temps = [float(r.get('temperatura', 0)) for r in ambiente_data if r.get('temperatura')]
            hums = [float(r.get('humedad', 0)) for r in ambiente_data if r.get('humedad')]
            
            total_registros = len(ambiente_data)
            temp_promedio = sum(temps) / len(temps) if temps else 0
            temp_maxima = max(temps) if temps else 0
            temp_minima = min(temps) if temps else 0
            hum_promedio = sum(hums) / len(hums) if hums else 0
            hum_maxima = max(hums) if hums else 0
            hum_minima = min(hums) if hums else 0
            
            # Contar activaciones de riego - revisar múltiples nombres posibles
            activaciones_riego = len([r for r in ambiente_data if 
                                     r.get('bomba') == 'Encendida' or 
                                     r.get('estado_bomba') == 'Encendida' or
                                     str(r.get('bomba', '')).lower() == 'encendida' or
                                     str(r.get('estado_bomba', '')).lower() == 'encendida'])
            
            # Datos de la tabla - exacto formato de la imagen
            data = [
                ['Métrica', 'Valor', 'Unidad'],
                ['Total de Registros', str(total_registros), 'registros'],
                ['Temperatura Promedio', f'{temp_promedio:.1f}', '°C'],
                ['Temperatura Máxima', f'{temp_maxima:.1f}', '°C'],
                ['Temperatura Mínima', f'{temp_minima:.1f}', '°C'],
                ['Humedad Promedio', f'{hum_promedio:.1f}', '%'],
                ['Humedad Máxima', f'{hum_maxima:.1f}', '%'],
                ['Humedad Mínima', f'{hum_minima:.1f}', '%'],
                ['Activaciones de Riego', str(activaciones_riego), 'veces'],
            ]
        
        # Crear tabla
        table = Table(data, colWidths=[4*cm, 2*cm, 2*cm])
        
        # Estilo de tabla
        table.setStyle(TableStyle([
            # Encabezado
            ('BACKGROUND', (0, 0), (-1, 0), self.colors['section_blue']),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.colors['white']),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            
            # Cuerpo de la tabla
            ('BACKGROUND', (0, 1), (-1, -1), self.colors['white']),
            ('TEXTCOLOR', (0, 1), (-1, -1), self.colors['text_black']),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),    # Métrica izquierda
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'), # Valor y unidad centrados
            
            # Bordes
            ('GRID', (0, 0), (-1, -1), 0.5, self.colors['border_gray']),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [self.colors['white'], self.colors['table_gray']]),
        ]))
        
        return table

    def create_detailed_table(self, ambiente_data, max_rows=20):
        """Crear tabla de registros detallados"""
        if not ambiente_data:
            return None
        
        # Tomar los últimos registros
        recent_data = ambiente_data[-max_rows:] if len(ambiente_data) > max_rows else ambiente_data
        
        # Encabezados de la tabla
        data = [['Fecha y Hora', 'Temperatura', 'Humedad', 'Estado Bomba', 'Alertas']]
        
        # Añadir datos
        for registro in recent_data:
            fecha = registro.get('fecha', '').replace('T', ' ').split('.')[0]
            temperatura = f"{float(registro.get('temperatura', 0)):.1f}°C"
            humedad = f"{float(registro.get('humedad', 0)):.1f}%"
            bomba = registro.get('bomba', 'Apagada')
            
            # Generar alertas basadas en valores
            alertas = []
            try:
                temp_val = float(registro.get('temperatura', 20))
                hum_val = float(registro.get('humedad', 50))
                
                if temp_val > 30:
                    alertas.append('Temperatura elevada')
                elif temp_val < 15:
                    alertas.append('Temperatura baja')
                
                if hum_val > 80:
                    alertas.append('Humedad alta')
                elif hum_val < 30:
                    alertas.append('Humedad baja')
            except:
                pass
            
            # Verificar si hay alertas existentes en el registro
            if registro.get('alerta') and registro.get('alerta').strip():
                alertas.append(registro.get('alerta'))
            
            alerta_text = ', '.join(alertas) if alertas else 'Sin alertas'
            
            data.append([fecha, temperatura, humedad, bomba, alerta_text])
        
        # Crear tabla
        table = Table(data, colWidths=[3.5*cm, 2*cm, 2*cm, 2.5*cm, 4*cm])
        
        # Estilo de tabla
        style_commands = [
            # Encabezado
            ('BACKGROUND', (0, 0), (-1, 0), self.colors['section_blue']),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.colors['white']),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            
            # Cuerpo de la tabla
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),    # Fecha
            ('ALIGN', (1, 1), (3, -1), 'CENTER'),  # Temperatura, Humedad, Bomba
            ('ALIGN', (4, 1), (4, -1), 'LEFT'),    # Alertas
            
            # Bordes
            ('GRID', (0, 0), (-1, -1), 0.5, self.colors['border_gray']),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]
        
        # Alternar colores de fila
        for i in range(1, len(data)):
            bg_color = self.colors['table_gray'] if i % 2 == 0 else self.colors['white']
            style_commands.append(('BACKGROUND', (0, i), (-1, i), bg_color))
            
            # Colorear alertas
            if 'elevada' in data[i][4] or 'alta' in data[i][4]:
                style_commands.append(('TEXTCOLOR', (4, i), (4, i), self.colors['red_alert']))
            elif 'baja' in data[i][4]:
                style_commands.append(('TEXTCOLOR', (4, i), (4, i), self.colors['orange_warning']))
            elif 'Sin alertas' in data[i][4]:
                style_commands.append(('TEXTCOLOR', (4, i), (4, i), self.colors['green_ok']))
        
        table.setStyle(TableStyle(style_commands))
        return table

    def generate_production_report(self, ambiente_data, seguridad_data=None, acceso_data=None, desde=None, hasta=None):
        """Generar reporte PDF con el diseño exacto de producción"""
        buffer = BytesIO()
        
        # Crear documento simple sin encabezados automáticos
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        story = []
        
        # === ENCABEZADO VERDE MANUAL ===
        header_data = [["■ REPORTE DEL INVERNADERO IoT"]]
        header_table = Table(header_data, colWidths=[doc.width])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.colors['header_green']),
            ('TEXTCOLOR', (0, 0), (-1, -1), self.colors['white']),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 18),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        story.append(header_table)
        
        # === INFORMACIÓN DEL SISTEMA ===
        fecha_info = f"Fecha de Generación: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
        version_info = "Versión: Control Automatizado de Invernadero"
        
        info_data = [[f"{fecha_info}\n{version_info}"]]
        info_table = Table(info_data, colWidths=[doc.width])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.colors['white']),
            ('TEXTCOLOR', (0, 0), (-1, -1), self.colors['text_black']),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, self.colors['border_gray']),
        ]))
        story.append(info_table)
        story.append(Spacer(1, 1*cm))
        # === RESUMEN EJECUTIVO ===
        # Crear título con fondo azul usando tabla
        section_title_data = [["■ RESUMEN EJECUTIVO"]]
        section_title_table = Table(section_title_data, colWidths=[doc.width])
        section_title_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.colors['section_blue']),
            ('TEXTCOLOR', (0, 0), (-1, -1), self.colors['white']),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 14),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(section_title_table)
        story.append(Spacer(1, 5*mm))
        
        # Tabla de resumen
        summary_table = self.create_summary_table(ambiente_data)
        if summary_table:
            story.append(summary_table)
        
        story.append(Spacer(1, 1*cm))
        
        # === REGISTROS DETALLADOS ===
        # Crear título con fondo azul usando tabla
        section_title_data2 = [["■ REGISTROS DETALLADOS"]]
        section_title_table2 = Table(section_title_data2, colWidths=[doc.width])
        section_title_table2.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.colors['section_blue']),
            ('TEXTCOLOR', (0, 0), (-1, -1), self.colors['white']),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 14),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(section_title_table2)
        story.append(Spacer(1, 5*mm))
        
        # Tabla de registros detallados
        detailed_table = self.create_detailed_table(ambiente_data)
        if detailed_table:
            story.append(detailed_table)
        
        # Nota al final
        story.append(Spacer(1, 1*cm))
        footer_note = Paragraph(
            "<i>Sistema de Automatización de Invernadero IoT - Generado automáticamente</i>",
            self.styles['Normal']
        )
        story.append(footer_note)
        
        # Nota final
        story.append(Spacer(1, 1*cm))
        footer_note = Paragraph(
            "<i>Sistema de Automatización de Invernadero IoT - Generado automáticamente</i>",
            self.styles['Normal']
        )
        story.append(footer_note)
        
        # Construir PDF sin encabezados/pies automáticos
        try:
            doc.build(story)
            buffer.seek(0)
            return buffer.getvalue()
        except Exception as e:
            print(f"Error generando PDF de producción: {e}")
            import traceback
            traceback.print_exc()
            return None


def generate_production_pdf_report(ambiente_data, seguridad_data=None, acceso_data=None, desde=None, hasta=None):
    """Función principal para generar PDF con diseño de producción"""
    try:
        generator = ProductionPDFGenerator()
        return generator.generate_production_report(ambiente_data, seguridad_data, acceso_data, desde, hasta)
    except Exception as e:
        print(f"Error en generador PDF de producción: {e}")
        return None