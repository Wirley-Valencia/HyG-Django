from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Product
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.utils import simpleSplit
from django.http import HttpResponse
# Register your models here.


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = ('id', 'title', 'description', 'price',
                    'created_at', 'expiration_date', 
                    'cantidad_disponible')
    list_editable = ('price','expiration_date', 'cantidad_disponible')
    search_fields = ('title', 'description')
    list_per_page = 9
    actions = ['generate_pdf']


    class ProductResource(resources.ModelResource):
        class Meta:
            model = Product
            fields = ('id', 'title', 'description', 'price',
                      'created_at', 'expiration_date', 'amount',
                      'cantidad_disponible')
            
            
    def generate_pdf(self, request, queryset):
        # Aquí llamamos a la función que genera el PDF
        pdf_response = self.generate_pdf_report(queryset)
        return pdf_response

    generate_pdf.short_description = "Generar PDF"

    def generate_pdf_report(self, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_productos.pdf"'

        # Create the PDF object with landscape orientation
        p = canvas.Canvas(response, pagesize=landscape(letter))

        # Coloca el logo una línea arriba del título
        logo_path = 'static/Iconos/H_G_Valencia.png'
        p.drawImage(logo_path, 50, 550, width=100, height=50)
        
        date_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        p.setFont("Helvetica", 8)
        p.drawRightString(770, 590, f"Generado el: {date_string}")

        # PDF Title
        p.setFont("Helvetica", 18)
        p.setFillColor(colors.darkblue) 
        p.drawString(100, 530, "Reporte de productos")  # Ajusta la coordenada Y aquí

        # Headers
        p.setFont("Helvetica", 10)
        p.setFillColor(colors.darkblue) 
        p.drawString(70, 500, "ID")
        p.drawString(130, 500, "Nombre")
        p.drawString(310, 500, "Precio")
        p.drawString(400, 500, "Cantidad")
        p.drawString(500, 500, "Fecha de Vencimiento")
        p.drawString(630, 500, "Estado")
        p.setFillColor(colors.black)

        # Content
        y_position = 470
        rows_per_page = 20  # Ajusta este valor según tu límite de filas por hoja
        for i, product in enumerate(queryset):
            if i % rows_per_page == 0 and i != 0:
                # Si alcanza el límite de filas por hoja, crea una nueva página
                p.showPage()
                    # Coloca el logo una línea arriba del título
                logo_path = 'static/Iconos/H_G_Valencia.png'
                p.drawImage(logo_path, 50, 550, width=100, height=50)
                
                date_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                p.setFont("Helvetica", 8)
                p.drawRightString(770, 590, f"Generado el: {date_string}")

        # PDF Title
                p.setFont("Helvetica", 16)
                p.setFillColor(colors.darkblue) 
                p.drawString(100, 530, "Reporte de productos")  # Ajusta la coordenada Y aquí

        # Headers
                p.setFont("Helvetica", 10)
                p.setFillColor(colors.darkblue) 
                p.drawString(70, 500, "ID")
                p.drawString(130, 500, "Nombre")
                p.drawString(310, 500, "Precio")
                p.drawString(400, 500, "Cantidad")
                p.drawString(500, 500, "Fecha de Vencimiento")
                p.drawString(630, 500, "Estado")
                p.setFillColor(colors.black)
                y_position = 470  # Reinicia la posición Y para la nueva página

            p.drawString(70, y_position, str(product.id))
            p.drawString(130, y_position, product.title)
            p.drawString(310, y_position, str(product.price))
            p.drawString(400, y_position, str(product.cantidad_disponible))
            p.drawString(500, y_position, product.expiration_date.strftime("%Y-%m-%d"))
            # """ p.drawString(600, y_position, str(product.expiration_date))
            # p.drawString(630, y_position, str(product.status)) """
            y_position -= 20
        
       


        # Close the PDF object cleanly, and we're done.
        p.showPage()
        p.save()

        return response


