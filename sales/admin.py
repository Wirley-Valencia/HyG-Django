from django.contrib import admin
from django.forms import ModelForm
from .models import DetalleVenta
from django.http import HttpResponse
from products.models import Product
from .models import Venta, DetalleVenta,Cliente
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.utils import simpleSplit

class DetalleVentaAdminForm(ModelForm):
    class Meta:
        model = DetalleVenta
        fields = '__all__'


class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1


@admin.register(Venta)
class VentaAdmin(ImportExportModelAdmin):
    inlines = [DetalleVentaInline]
    list_display = ('cliente', 'fecha', 'total')
    search_fields = ('cliente', 'fecha', 'total')
    actions = ['generate_pdf']
    
    class VencimientoResource(resources.ModelResource):
        class Meta:
            model = Venta
            fields = ('cliente', 'fecha', 'total')
            
    def generate_pdf(self, request, queryset):
        # Aquí llamamos a la función que genera el PDF
        pdf_response = self.generate_pdf_report(queryset)
        return pdf_response

    generate_pdf.short_description = "Generar PDF"

    def generate_pdf_report(self, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="ventas_report.pdf"'

        # Create the PDF object, using the response object as its "file."
        p = canvas.Canvas(response, pagesize=letter)

        logo_path = 'static/Iconos/H_G_Valencia.png'
        p.drawImage(logo_path, 50, 730, width=100, height=50)

        date_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        p.setFont("Helvetica", 8)
        p.drawRightString(600, 730, f"Generado el: {date_string}")

        # PDF Title
        p.setFont("Helvetica", 16)
        p.setFillColor(colors.darkblue)
        p.drawString(100, 700, "Reporte de ventas")

        # Headers
        p.setFont("Helvetica", 10)
        p.setFillColor(colors.darkblue)
        p.drawString(70, 675, "ID Venta")
        p.drawString(150, 675, "ID Cliente")
        p.drawString(300, 675, "Fecha")
        p.drawString(450, 675, "Total")
        p.setFillColor(colors.black)

        # Content
        y_position = 645
        rows_per_page = 20  # Ajusta este valor según tu límite de filas por hoja
        for i, venta in enumerate(queryset):
            if i % rows_per_page == 0 and i != 0:
                # Si alcanza el límite de filas por hoja, crea una nueva página
                p.showPage()
                logo_path = 'static/Iconos/iconopdf.png'
                p.drawImage(logo_path, 50, 730, width=100, height=50)

                date_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                p.setFont("Helvetica", 8)
                p.drawRightString(300, 730, f"Generado el: {date_string}")

                # PDF Title
                p.setFont("Helvetica", 16)
                p.setFillColor(colors.darkblue)
                p.drawString(150, 730, "Reporte de ventas")

                # Resto del código para el encabezado de la nueva página
                p.setFont("Helvetica", 16)
                p.drawString(100, 800, "Reporte de ventas")
                p.setFont("Helvetica", 10)
                p.drawString(70, 780, "ID Venta")
                p.drawString(150, 780, "ID Cliente")
                p.drawString(300, 780, "Fecha")
                p.drawString(450, 780, "Total")
                y_position = 760  # Reinicia la posición Y para la nueva página

            p.drawString(70, y_position, str(venta.id))
            p.drawString(150, y_position, str(venta.cliente.nombre))
            p.drawString(300, y_position, str(venta.fecha))
            p.drawString(450, y_position, str(venta.total))
            y_position -= 20

        # Close the PDF object cleanly, and we're done.
        p.showPage()
        p.save()

        return response

@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    form = DetalleVentaAdminForm
    list_display = ('id', 'venta', 'producto', 'cantidad', 'subtotal')
    search_fields = ['venta__cliente__nombre', 'producto__nombre']

    readonly_fields = ('producto', 'cantidad', 'subtotal')
    
    class Media:
        js = ('sales/admin/js/admin.js',)


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'telefono')
