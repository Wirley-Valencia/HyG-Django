from django.contrib import admin
from django.http import HttpResponse
from .models import Compra,  Suppliers, Gastos
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.utils import simpleSplit
from products.models import Product

@admin.register(Compra)
class CompraAdmin(ImportExportModelAdmin):
    list_display = ('id', 'supplier', 'product', 'datec',
                    'amountc', 'pricec', 'description',)
    list_editable = ('supplier', 'product',)
    search_fields = ('supplier', 'product',)
    list_per_page = 9
    actions = ['generate_pdf']
    
    class CompraResource(resources.ModelResource):
        class Meta:
            model = Compra
            fields = ('id', 'supplier', 'product', 'datec',
                    'amountc', 'pricec', 'description',)
    
    def generate_pdf(self, request, queryset):
      
        pdf_response_products = self.generate_pdf_report(queryset)
        

        queryset_compra = Compra.objects.all()  
        pdf_response_compra = self.generate_pdf_report_compras(queryset_compra)


        pdf_response_products.write(pdf_response_compra)

     
        return pdf_response_compra

    generate_pdf.short_description = "Generar PDF"

    def generate_pdf_report(self, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_productos.pdf"'


        return response

    def generate_pdf_report_compras(self, queryset_compra):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_compras.pdf"'

        
        p = canvas.Canvas(response, pagesize=landscape(letter))

 
        logo_path = 'static/Iconos/H_G_Valencia.png'
        p.drawImage(logo_path, 50, 550, width=100, height=50)
        
        date_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        p.setFont("Helvetica", 8)
        p.drawRightString(770, 590, f"Generado el: {date_string}")

       
        p.setFont("Helvetica", 18)
        p.setFillColor(colors.darkblue) 
        p.drawString(100, 530, "Reporte de compras")  

        
        p.setFont("Helvetica", 10)
        p.setFillColor(colors.darkblue) 
        p.drawString(70, 500, "ID")
        p.drawString(120, 500, "Descripción")
        p.drawString(320, 500, "Cantidad")
        p.drawString(400, 500, "Fecha")
        p.drawString(500, 500, "Precio")
        p.drawString(580, 500, "Proveedor")
        p.drawString(680, 500, "Producto")
        p.setFillColor(colors.black)

       
        y_position = 470
        rows_per_page = 20  
        for i, compra in enumerate(queryset_compra):
            if i % rows_per_page == 0 and i != 0:
                
                p.showPage()
                
                logo_path = 'static/Iconos/iconopdf.png'
                p.drawImage(logo_path, 50, 550, width=100, height=50)
                
                date_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                p.setFont("Helvetica", 8)
                p.drawRightString(770, 590, f"Generado el: {date_string}")

                p.setFont("Helvetica", 18)
                p.setFillColor(colors.darkblue) 
                p.drawString(100, 530, "Reporte de compras") 

                
                p.setFont("Helvetica", 10)
                p.setFillColor(colors.darkblue) 
                p.drawString(70, 500, "ID")
                p.drawString(120, 500, "Descripción")
                p.drawString(320, 500, "Cantidad")
                p.drawString(400, 500, "Fecha")
                p.drawString(500, 500, "Precio")
                p.drawString(580, 500, "Proveedor")
                p.drawString(680, 500, "Producto")
                p.setFillColor(colors.black)
                y_position = 470  

            p.drawString(70, y_position, str(compra.id))
            p.drawString(120, y_position, compra.description)
            p.drawString(330, y_position, str(compra.amountc))
            p.drawString(400, y_position, str(compra.datec))
            p.drawString(500, y_position, str(compra.pricec))
            p.drawString(580, y_position, compra.supplier.name)  
            p.drawString(680, y_position, compra.product.title)
            y_position -= 20
            
            

        p.showPage()
        p.save()

        return response
    
    
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
        
        pdf_response = self.generate_pdf_report(queryset)
        return pdf_response

    generate_pdf.short_description = "Generar PDF"

    def generate_pdf_report(self, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_gastos.pdf"'

        p = canvas.Canvas(response, pagesize=letter)

        logo_path = 'static/Iconos/H_G_Valencia.png'
        p.drawImage(logo_path, 50, 730, width=100, height=50)
        
        date_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        p.setFont("Helvetica", 8)
        p.drawRightString(600, 730, f"Generado el: {date_string}")

      
        p.setFont("Helvetica", 16) 
        p.setFillColor(colors.darkblue) 
        p.drawString(100, 700, "Reporte de gastos")

       
        p.setFont("Helvetica", 10)
        p.setFillColor(colors.darkblue) 
        p.drawString(70, 675, "ID")
        p.drawString(150, 675, "Descripción")
        p.drawString(450, 675, "Fecha")
        p.drawString(530, 675, "Precio")
        p.setFillColor(colors.black)

        
        y_position = 645
        rows_per_page = 20  
        for i, gasto in enumerate(queryset):
            if i % rows_per_page == 0 and i != 0:
                
                p.showPage()
                logo_path = 'static/Iconos/iconopdf.png'
                p.drawImage(logo_path, 50, 730, width=100, height=50)
                
                date_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                p.setFont("Helvetica", 8)
                p.drawRightString(300, 730, f"Generado el: {date_string}")

                p.setFont("Helvetica", 16) 
                p.setFillColor(colors.darkblue) 
                p.drawString(150, 730, "Reporte de gastos")

                p.setFont("Helvetica", 16)
                p.drawString(100, 800, "Reporte de gastos")
                p.setFont("Helvetica", 10)
                p.drawString(70, 780, "ID")
                p.drawString(150, 780, "Descripción")
                p.drawString(450, 780, "Fecha")
                p.drawString(530, 780, "Precio")
                y_position = 760  

            
            p.drawString(70, y_position, str(gasto.id))
            p.drawString(150, y_position, gasto.description)
            p.drawString(440, y_position, str(gasto.date))
            p.drawString(530, y_position, str(gasto.price))
            y_position -= 20

        p.showPage()
        p.save()

        return response

class CompraResource(resources.ModelResource):
    class Meta:
        model = Compra
        fields = ('id', 'supplier', 'product', 'datec',
                  'amountc', 'pricec', 'description',)


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

        logo_path = 'static/Iconos/H_G_Valencia.png'
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
                logo_path = 'static/Iconos/iconopdf.png'
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

