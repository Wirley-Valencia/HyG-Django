from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Product, Stock
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape, portrait
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.utils import simpleSplit
from django.http import HttpResponse
from django.db import models
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

class StockInline(admin.TabularInline):
    model = Stock
    extra = 1

class ProductAdmin(ImportExportModelAdmin):
    list_display = ('id', 'title', 'description', 'price',  'status', 'total_cantidad_disponible')
    list_editable = ( 'price', 'status', )
    search_fields = ('title', 'description', 'status', )
    list_per_page = 9
    inlines = [StockInline]
    actions = ['generate_pdf']
    exclude = ['slug','total_cantidad_disponible']

    class ProductResource(resources.ModelResource):
        class Meta:
            model = Product
            fields = ('id', 'title', 'description', 'price', 'created_at', 'status', 'total_cantidad_disponible')
        
    def generate_pdf(self, request, queryset):
        pdf_response_products = self.generate_pdf_report_products(queryset)
        return pdf_response_products

    def generate_pdf_report_products(self, queryset_products):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_inventario.pdf"'

        p = canvas.Canvas(response, pagesize=portrait(letter))

        logo_path = 'static/Iconos/icono_pdf.jpg'
        date_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.draw_header(p, logo_path, date_string)
        self.draw_table_header(p)

        y_position = 645
        rows_per_page = 20
        
        
        for i, products in enumerate(queryset_products):
            if i % rows_per_page == 0 and i != 0:
                p.showPage()  # Crear una nueva página
                self.draw_header(p, logo_path, date_string)  # Dibujar el encabezado en la nueva página
                self.draw_table_header(p)  # Dibujar el encabezado de la tabla en la nueva página
                y_position =  645 # Restablecer la posición Y

            self.draw_compra_details(p, products, y_position)  # Dibujar los detalles del proveedor
            y_position -= 45  # Ajustar la posición Y para la siguiente fila


        p.save()

        return response

    def draw_header(self, canvas, logo_path, date_string):
        canvas.drawImage(logo_path, 50, 730, width=150, height=50)
        canvas.setFont("Helvetica", 8)
        canvas.drawRightString(600, 730, f"Generado el: {date_string}")
        canvas.setFont("Helvetica", 18)
        canvas.setFillColor(colors.darkblue)
        canvas.drawString(100, 700, "Reporte de Inventario")

    def draw_table_header(self, canvas):
        canvas.setFont("Helvetica", 10)
        canvas.setFillColor(colors.darkblue)
        canvas.drawString(70, 675, "ID")
        canvas.drawString(100, 675, "Nombre Producto")
        canvas.drawString(310, 675, "Precio")
        canvas.drawString(380, 675, "Cantidad")
        canvas.drawString(460, 675, "Estado")
    
        canvas.setFillColor(colors.black)

    def draw_compra_details(self, canvas, products, y_position):
        canvas.drawString(70, y_position, str(products.id))
        canvas.drawString(100, y_position, str(products.title))
        canvas.drawString(310, y_position, str(products.price))
        canvas.drawString(380, y_position, str(products.total_cantidad_disponible))
        canvas.drawString(460, y_position, str(products.status))

    
    
admin.site.register(Product, ProductAdmin)
    

class StockAdmin(ImportExportModelAdmin):
    list_display = ('id', 'product', 'expiration_date', 'cantidad_disponible', 'codigo', 'status',)
    list_editable = ('expiration_date', 'cantidad_disponible')
    search_fields = ('product__title',)
    list_per_page = 9
    actions = ['generate_pdf']
    
    class StockResource(resources.ModelResource):
        class Meta:
            model = Stock
            fields = ('id', 'product', 'expiration_date', 'cantidad_disponible', 'codigo')
            
    def generate_pdf(self, request, queryset):
        pdf_response_stock = self.generate_pdf_report_stock(queryset)
        return pdf_response_stock

    def generate_pdf_report_stock(self, queryset_stock):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_stock.pdf"'

        p = canvas.Canvas(response, pagesize=portrait(letter))

        logo_path = 'static/Iconos/icono_pdf.jpg'
        date_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.draw_header(p, logo_path, date_string)
        self.draw_table_header(p)

        y_position = 645
        rows_per_page = 20
        
        
        for i, stock in enumerate(queryset_stock):
            if i % rows_per_page == 0 and i != 0:
                p.showPage()  # Crear una nueva página
                self.draw_header(p, logo_path, date_string)  # Dibujar el encabezado en la nueva página
                self.draw_table_header(p)  # Dibujar el encabezado de la tabla en la nueva página
                y_position =  645 # Restablecer la posición Y

            self.draw_compra_details(p, stock, y_position)  # Dibujar los detalles del proveedor
            y_position -= 45  # Ajustar la posición Y para la siguiente fila


        p.save()

        return response

    def draw_header(self, canvas, logo_path, date_string):
        canvas.drawImage(logo_path, 50, 730, width=150, height=50)
        canvas.setFont("Helvetica", 8)
        canvas.drawRightString(600, 730, f"Generado el: {date_string}")
        canvas.setFont("Helvetica", 18)
        canvas.setFillColor(colors.darkblue)
        canvas.drawString(100, 700, "Reporte de stocks")

    def draw_table_header(self, canvas):
        canvas.setFont("Helvetica", 10)
        canvas.setFillColor(colors.darkblue)
        canvas.drawString(55, 675, "ID")
        canvas.drawString(90, 675, "Producto")
        canvas.drawString(230, 675, "Codigo")
        canvas.drawString(305, 675, "Cantidad disponible")
        canvas.drawString(400, 675, "Fecha De Vencimiento")
        canvas.drawString(530, 675, "Estado")
    
        canvas.setFillColor(colors.black)

    def draw_compra_details(self, canvas, stock, y_position):
        canvas.drawString(55, y_position, str(stock.id))
        canvas.drawString(90, y_position, str(stock.product))
        canvas.drawString(230, y_position, str(stock.codigo))
        canvas.drawString(320, y_position, str(stock.cantidad_disponible))
        canvas.drawString(400, y_position, str(stock.expiration_date))  
        canvas.drawString(530, y_position, str(stock.status)) 
            
    
admin.site.register(Stock, StockAdmin)
    


