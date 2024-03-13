from django.contrib import admin
from django.http import HttpResponse
from .models import Compra,  Suppliers, Gastos
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape, portrait
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.utils import simpleSplit
from products.models import Product
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


@admin.register(Compra)
class CompraAdmin(ImportExportModelAdmin):
    list_display = ('id', 'supplier', 'datec',
                    'amountc', 'pricec', 'description',)
    list_editable = ('datec', )
    search_fields = ('datec', 'supplier__name',)
    list_per_page = 9
    actions = ['generate_pdf']
    
    
    
    class CompraResource(resources.ModelResource):
        class Meta:
            model = Compra
            fields = ('id', 'supplier',  'datec',
                    'amountc', 'pricec', 'description',)
    
    def generate_pdf(self, request, queryset):
        pdf_response_compra = self.generate_pdf_report_compras(queryset)
        return pdf_response_compra

    def generate_pdf_report_compras(self, queryset_compra):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_compras.pdf"'

        p = canvas.Canvas(response, pagesize=landscape(letter))

        logo_path = 'static/Iconos/icono_pdf.jpg'
        date_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.draw_header(p, logo_path, date_string)
        self.draw_table_header(p)

        y_position = 470
        rows_per_page = 10
        total_price = 0 
        
        for i, compra in enumerate(queryset_compra):
            if i % rows_per_page == 0 and i != 0:
                p.showPage()  # Crear una nueva página
                self.draw_header(p, logo_path, date_string)  # Dibujar el encabezado en la nueva página
                self.draw_table_header(p)  # Dibujar el encabezado de la tabla en la nueva página
                y_position =  470  # Restablecer la posición Y

            self.draw_compra_details(p, compra, y_position)
            total_price += compra.pricec
            y_position -= 45

        self.draw_total_price(p, total_price)

        p.save()

        return response

    def draw_header(self, canvas, logo_path, date_string):
        canvas.drawImage(logo_path, 50, 550, width=150, height=50)
        canvas.setFont("Helvetica", 8)
        canvas.drawRightString(770, 590, f"Generado el: {date_string}")
        canvas.setFont("Helvetica", 18)
        canvas.setFillColor(colors.darkblue)
        canvas.drawString(330, 530, "Reporte de compras")

    def draw_table_header(self, canvas):
        canvas.setFont("Helvetica", 10)
        canvas.setFillColor(colors.darkblue)
        canvas.drawString(70, 500, "ID")
        canvas.drawString(105, 500, "Descripción")
        canvas.drawString(320, 500, "Cantidad")
        canvas.drawString(400, 500, "Fecha")
        canvas.drawString(500, 500, "Precio")
        canvas.drawString(580, 500, "Proveedor")
        canvas.setFillColor(colors.black)

    def draw_compra_details(self, canvas, compra, y_position):
        canvas.drawString(70, y_position, str(compra.id))

        # Ajustar el texto de la descripción para que se ajuste automáticamente
        description_width = 220  # Ancho máximo para la descripción
        description = compra.description
        text_object = canvas.beginText(105, y_position)
        text_object.setFont("Helvetica", 10)  # Ajustar el tamaño de la fuente si es necesario
        text_object.setLeading(11)  # Espaciado entre líneas

        lines = self.wrap_text(description, description_width)  # Eliminamos el argumento canvas
        for line in lines:
            text_object.textLine(line)

        canvas.drawText(text_object)

        canvas.drawString(330, y_position, str(compra.amountc))
        canvas.drawString(400, y_position, str(compra.datec))
        canvas.drawString(500, y_position, str(compra.pricec))
        canvas.drawString(580, y_position, compra.supplier.name)

    def wrap_text(self, text, width):
        lines = []
        current_line = ''

        for word in text.split():
            if pdfmetrics.stringWidth(current_line + ' ' + word, "Helvetica", 10) < width:
                current_line += ' ' + word
            else:
                lines.append(current_line.strip())
                current_line = word

        lines.append(current_line.strip())

        return lines
    
    def draw_total_price(self, canvas, total_price):
        # Define el color personalizado para el fondo del rectángulo
        light_sky_blue = colors.Color(0.53, 0.81, 0.98)  # RGB para LightSkyBlue

        # Dibuja el rectángulo de fondo azul claro
        canvas.setFillColor(light_sky_blue)
        canvas.rect(330, 10, 100, 30, fill=True, stroke=False)

        # Dibuja el texto del total dentro del rectángulo
        canvas.setFillColor(colors.black)
        canvas.setFont("Helvetica", 12)
        canvas.drawString(350, 20, f"Total : {total_price}")

    
    
@admin.register(Gastos)   
class GastosAdmin(ImportExportModelAdmin):
    list_display = ('id', 'description', 'date', 'price',)
    list_editable = ('description', 'date', 'price',)
    search_fields = ('description',)
    list_per_page = 9

    actions = ['generate_pdf']
    
    class GastosResource(resources.ModelResource):
        class Meta:
            model = Gastos
            fields = ('id', 'description', 'date', 'price',)
            
    def generate_pdf(self, request, queryset):
        pdf_response_compra = self.generate_pdf_report_gastos(queryset)
        return pdf_response_compra

    def generate_pdf_report_gastos(self, queryset_gastos):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_gastos.pdf"'

        p = canvas.Canvas(response, pagesize=portrait(letter))

        logo_path = 'static/Iconos/icono_pdf.jpg'
        date_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.draw_header(p, logo_path, date_string)
        self.draw_table_header(p)

        y_position = 625
        rows_per_page = 11
        total_price = 0 
        
        for i, gastos in enumerate(queryset_gastos):
            if i % rows_per_page == 0 and i != 0:
                p.showPage()  # Crear una nueva página
                self.draw_header(p, logo_path, date_string)  # Dibujar el encabezado en la nueva página
                self.draw_table_header(p)  # Dibujar el encabezado de la tabla en la nueva página
                y_position =  625 # Restablecer la posición Y

            self.draw_compra_details(p, gastos, y_position)
            total_price += gastos.price
            y_position -= 45

        self.draw_total_price(p, total_price)

        p.save()

        return response

    def draw_header(self, canvas, logo_path, date_string):
        canvas.drawImage(logo_path, 50, 730, width=150, height=50)
        canvas.setFont("Helvetica", 8)
        canvas.drawRightString(600, 730, f"Generado el: {date_string}")
        canvas.setFont("Helvetica", 18)
        canvas.setFillColor(colors.darkblue)
        canvas.drawString(100, 700, "Reporte de gastos")

    def draw_table_header(self, canvas):
        canvas.setFont("Helvetica", 10)
        canvas.setFillColor(colors.darkblue)
        canvas.drawString(70, 675, "ID")
        canvas.drawString(150, 675, "Descripción")
        canvas.drawString(450, 675, "Fecha")
        canvas.drawString(530, 675, "Precio")
    
        canvas.setFillColor(colors.black)

    def draw_compra_details(self, canvas, gastos, y_position):
        canvas.drawString(70, y_position, str(gastos.id))

        # Ajustar el texto de la descripción para que se ajuste automáticamente
        description_width = 220  # Ancho máximo para la descripción
        description = gastos.description
        text_object = canvas.beginText(150, y_position)
        text_object.setFont("Helvetica", 10)  # Ajustar el tamaño de la fuente si es necesario
        text_object.setLeading(11)  # Espaciado entre líneas

        lines = self.wrap_text(description, description_width)  # Eliminamos el argumento canvas
        for line in lines:
            text_object.textLine(line)

        canvas.drawText(text_object)

        canvas.drawString(440, y_position, str(gastos.date))
        canvas.drawString(530, y_position, str(gastos.price))
  

    def wrap_text(self, text, width):
        lines = []
        current_line = ''

        for word in text.split():
            if pdfmetrics.stringWidth(current_line + ' ' + word, "Helvetica", 10) < width:
                current_line += ' ' + word
            else:
                lines.append(current_line.strip())
                current_line = word

        lines.append(current_line.strip())

        return lines
    
    def draw_total_price(self, canvas, total_price):
        # Define el color personalizado para el fondo del rectángulo
        light_sky_blue = colors.Color(0.53, 0.81, 0.98)  # RGB para LightSkyBlue

        # Dibuja el rectángulo de fondo azul claro
        canvas.setFillColor(light_sky_blue)
        canvas.rect(290, 15, 100, 40, fill=True, stroke=False)

        # Dibuja el texto del total dentro del rectángulo
        canvas.setFillColor(colors.black)
        canvas.setFont("Helvetica", 12)
        canvas.drawString(300, 30, f"Total : {total_price}")




@admin.register(Suppliers)
class SuppliersAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'email', 'phone',)
    list_editable = ('email', 'phone',)
    actions = ['generate_pdf']
    
    class SuppliersResource(resources.ModelResource):
        class Meta:
            model = Suppliers
            fields = ('id', 'name', 'email', 'phone',)
            
    def generate_pdf(self, request, queryset):
        
        pdf_response = self.generate_pdf_report(queryset)
        return pdf_response

    generate_pdf.short_description = "Generar PDF"

    def generate_pdf_report(self, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_proveedores.pdf"'

        
        p = canvas.Canvas(response, pagesize=letter)

        logo_path = 'static/Iconos/icono_pdf.jpg'
        p.drawImage(logo_path, 50, 730, width=100, height=50)

        date_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        p.setFont("Helvetica", 8)
        p.drawRightString(600, 730, f"Generado el: {date_string}")

        p.setFont("Helvetica", 16)
        p.setFillColor(colors.darkblue)
        p.drawString(100, 700, "Reporte de proveedores")

        p.setFont("Helvetica", 10)
        p.setFillColor(colors.darkblue)
        p.drawString(70, 675, "ID")
        p.drawString(150, 675, "Nombre")
        p.drawString(280, 675, "Email")
        p.drawString(480, 675, "Teléfono")
        p.setFillColor(colors.black)

        y_position = 645
        rows_per_page = 20  
        for i, supplier in enumerate(queryset):
            if i % rows_per_page == 0 and i != 0:
                
                p.showPage()
                logo_path = 'static/Iconos/icono_pdf.jpg'
                p.drawImage(logo_path, 50, 730, width=100, height=50)

                date_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                p.setFont("Helvetica", 8)
                p.drawRightString(300, 730, f"Generado el: {date_string}")

                
                p.setFont("Helvetica", 16)
                p.setFillColor(colors.darkblue)
                p.drawString(150, 730, "Reporte de proveedores")

                
                p.setFont("Helvetica", 16)
                p.drawString(100, 800, "Reporte de proveedores")
                p.setFont("Helvetica", 10)
                p.drawString(70, 780, "ID")
                p.drawString(150, 780, "Nombre")
                p.drawString(280, 780, "Email")
                p.drawString(480, 780, "Teléfono")
                y_position = 760  

            p.drawString(70, y_position, str(supplier.id))
            p.drawString(150, y_position, supplier.name)
            p.drawString(280, y_position, supplier.email)
            p.drawString(480, y_position, supplier.phone)
            y_position -= 20

        
        p.showPage()
        p.save()

        return response

