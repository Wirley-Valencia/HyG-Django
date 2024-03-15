from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Product, Stock
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.utils import simpleSplit
from django.http import HttpResponse
from django.db import models


class StockInline(admin.TabularInline):
    model = Stock
    extra = 1

class ProductAdmin(ImportExportModelAdmin):
    list_display = ('id', 'title', 'description', 'price',  'status', 'total_cantidad_disponible')
    list_editable = ( 'price', 'status', 'total_cantidad_disponible')
    search_fields = ('title', 'description', 'status', )
    list_per_page = 9
    inlines = [StockInline]
    actions = ['generate_pdf']
    exclude = ['slug']

    class ProductResource(resources.ModelResource):
        class Meta:
            model = Product
            fields = ('id', 'title', 'description', 'price', 'created_at', 'status', 'total_cantidad_disponible')
        
    def generate_pdf(self, request, queryset):
       
        pdf_response = self.generate_pdf_report(queryset)
        return pdf_response

    generate_pdf.short_description = "Generar PDF"

    def generate_pdf_report(self, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_productos.pdf"'

        
        p = canvas.Canvas(response, pagesize=landscape(letter))

        
        logo_path = 'static/Iconos/icono_pdf.jpg'
        p.drawImage(logo_path, 50, 550, width=100, height=50)
        
        date_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        p.setFont("Helvetica", 8)
        p.drawRightString(770, 590, f"Generado el: {date_string}")

        
        p.setFont("Helvetica", 18)
        p.setFillColor(colors.darkblue) 
        p.drawString(100, 530, "Reporte de productos")  

        
        p.setFont("Helvetica", 10)
        p.setFillColor(colors.darkblue) 
        p.drawString(70, 500, "ID")
        p.drawString(130, 500, "Nombre")
        p.drawString(310, 500, "Precio")
        p.drawString(400, 500, "Cantidad")
        p.drawString(500, 500, "Estado")
        p.setFillColor(colors.black)

        
        y_position = 470
        rows_per_page = 20  
        for i, product in enumerate(queryset):
            if i % rows_per_page == 0 and i != 0:
                
                p.showPage()
                    
                logo_path = 'static/Iconos/icono_pdf.jpg'
                p.drawImage(logo_path, 50, 550, width=100, height=50)
                
                date_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                p.setFont("Helvetica", 8)
                p.drawRightString(770, 590, f"Generado el: {date_string}")

        
                p.setFont("Helvetica", 16)
                p.setFillColor(colors.darkblue) 
                p.drawString(100, 530, "Reporte de productos")  

        
                p.setFont("Helvetica", 10)
                p.setFillColor(colors.darkblue) 
                p.drawString(70, 500, "ID")
                p.drawString(130, 500, "Nombre")
                p.drawString(310, 500, "Precio")
                p.drawString(400, 500, "Cantidad")
                p.drawString(500, 500, "Estado")
                p.setFillColor(colors.black)
                y_position = 470  

            p.drawString(70, y_position, str(product.id))
            p.drawString(130, y_position, product.title)
            p.drawString(310, y_position, str(product.price))
            p.drawString(400, y_position, str(product.total_cantidad_disponible))
            p.drawString(500, y_position, product.status)
            # """ p.drawString(600, y_position, str(product.expiration_date))
            # p.drawString(630, y_position, str(product.status)) """
            y_position -= 20
        
       

        p.showPage()
        p.save()

        return response

admin.site.register(Product, ProductAdmin)
    


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'expiration_date', 'cantidad_disponible')
    list_editable = ('expiration_date', 'cantidad_disponible')
    search_fields = ('product__title',)
    list_per_page = 9
            
    


