from django.contrib import admin
from django.forms import ModelForm
from .models import DetalleVenta
from django.http import HttpResponse
from products.models import Product
from .models import Venta, DetalleVenta,Cliente
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape, portrait
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.utils import simpleSplit
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from django.conf import settings
from email.mime.text import MIMEText

class DetalleVentaAdminForm(ModelForm):
    class Meta:
        model = DetalleVenta
        fields = '__all__'


class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1
    

        
class FacturaPDF:
    def generate_pdf(self, venta_id):
        venta = Venta.objects.get(pk=venta_id)
        cliente = venta.cliente
        detalles_venta = venta.detalleventa_set.all()

        pdf_response = HttpResponse(content_type='application/pdf')
        pdf_response['Content-Disposition'] = f'attachment; filename="factura_{venta_id}.pdf"'
        
        logo_path = 'static/Iconos/icono_pdf.jpg'
        date_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        p = canvas.Canvas(pdf_response, pagesize=portrait(letter))

      
        self.draw_header(p, logo_path, date_string)
        self.draw_cliente_info(p, cliente, venta)
        self.draw_detalle_venta(p, detalles_venta)

        p.showPage()
        p.save()
        
        mensaje = "Adjunto encontrarás la factura de tu compra. ¡Gracias por tu Compra!"
        self.enviar_factura_por_correo(cliente.email, pdf_response.content, mensaje)

        
        return pdf_response
    
    def enviar_factura_por_correo(venta_id, cliente_email, factura_pdf, mensaje):
    # Configuración del servidor SMTP
        smtp_server = settings.EMAIL_HOST
        smtp_port = settings.EMAIL_PORT
        smtp_username = settings.EMAIL_HOST_USER
        smtp_password = settings.EMAIL_HOST_PASSWORD

        # Dirección de correo electrónico del remitente
        remitente = settings.EMAIL_HOST_USER

        # Crear el mensaje de correo electrónico
        msg = MIMEMultipart()
        msg['From'] = remitente
        msg['To'] = cliente_email
        msg['Subject'] = "Factura de compra"

        # Adjuntar el archivo PDF de la factura al correo electrónico
        adjunto = MIMEBase('application', 'octet-stream')
        adjunto.set_payload(factura_pdf)
        encoders.encode_base64(adjunto)
        adjunto.add_header('Content-Disposition', f'attachment; filename=factura_{venta_id}.pdf')
        msg.attach(adjunto)
        
         # Agregar el mensaje al cuerpo del correo electrónico
        mensaje_correo = MIMEText(mensaje)
        msg.attach(mensaje_correo)

        
        

        # Iniciar la conexión SMTP y enviar el correo electrónico
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(remitente, cliente_email, msg.as_string())
            server.quit()
            return True
        except Exception as e:
            print(f"Error al enviar el correo electrónico: {e}")
            return False
     

    def draw_header(self, canvas, logo_path, date_string):
        canvas.drawImage(logo_path, 50, 730, width=150, height=50)
        canvas.setFont("Helvetica", 8)
        canvas.drawRightString(600, 730, f"Generado el: {date_string}")
        canvas.setFont("Helvetica", 18)
        canvas.setFillColor(colors.darkblue)
        canvas.drawString(250, 700, "Factura De Compra")
        canvas.setFillColor(colors.black)

    def draw_cliente_info(self, canvas, cliente, venta):
        
        canvas.setFont("Helvetica", 12)
        canvas.setFillColor(colors.black)
        canvas.drawString(50, 660, f"Cliente: {cliente.nombre}")
        canvas.drawString(50, 640, f"Email: {cliente.email}")
        if cliente.telefono:
            canvas.drawString(50, 620, f"Teléfono: {cliente.telefono}")
        canvas.drawString(50, 580, f"TOTAL DE LA COMPRA: {venta.total}")

    def draw_detalle_venta(self, canvas, detalles_venta):
        canvas.setFont("Helvetica", 12)
        
        y_position = 510
        canvas.setFillColor(colors.darkblue)
        canvas.drawString(70, 540, "PRODUCTOS")
        canvas.drawString(250, 540, "CANTIDAD")
        canvas.drawString(450, 540, "SUBTOTAL")
        canvas.setFillColor(colors.black)
        for detalle in detalles_venta:
            canvas.drawString(70, y_position, f"{detalle.producto.title}")
            canvas.drawString(270, y_position, f" {detalle.cantidad}")
            canvas.drawString(450, y_position, f" {detalle.subtotal}")
            y_position -= 20
            
   

    
    

            
@admin.register(Venta)
class VentaAdmin(ImportExportModelAdmin):
    inlines = [DetalleVentaInline]
    list_display = ('cliente', 'fecha', 'total')
    search_fields = ('cliente', 'fecha', 'total')
    actions = ['generate_pdf','generate_invoice']
    
    class VencimientoResource(resources.ModelResource):
        class Meta:
            model = Venta
            fields = ('cliente', 'fecha', 'total')
    
    def generate_invoice(self, request, queryset):
        for venta in queryset:
            factura_pdf = FacturaPDF()
            pdf_response = factura_pdf.generate_pdf(venta.id)
            return pdf_response
    
    generate_invoice.short_description = "Generar factura"
    
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

        logo_path = 'static/Iconos/icono_pdf.jpg'
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
        p.drawString(150, 675, "Cliente")
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
                logo_path = 'static/Iconos/icono_pdf.jpg'
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
    
    #PDF DE LA FACTURA
    def factura_pdf(self, request, queryset):
        # Aquí llamamos a la función que genera el PDF
        pdf_response = self.factura_pdf_report(queryset)
        return pdf_response

    factura_pdf.short_description = "Factura PDF"

    def factura_pdf_report(self, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Factura.pdf"'

        # Create the PDF object, using the response object as its "file."
        p = canvas.Canvas(response, pagesize=letter)

        logo_path = 'static/Iconos/icono_pdf.jpg'
        p.drawImage(logo_path, 50, 730, width=100, height=50)

        date_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        p.setFont("Helvetica", 8)
        p.drawRightString(600, 760, f"Generado el: {date_string}")

        # PDF Title
        p.setFont("Helvetica", 20)
        p.setFillColor(colors.darkblue)
        p.drawString(250, 750, "Factura")

        # Headers
        p.setFont("Helvetica", 12)
        p.setFillColor(colors.darkblue)
        p.drawString(70, 670, "ID Venta: ")
        p.drawString(350, 670, "Cliente: ")
        p.drawString(70, 650, "Fecha: ")
        p.drawString(350, 650, "Total: ")
        
        p.drawString(60, 600, " No ")
        p.drawString(100, 600, " PRODUCTO ")
        p.drawString(290, 600, " CANTIDAD ")
        p.drawString(470, 600, " SUBTOTAL ")
        p.setFillColor(colors.black)

        # Content
        y_position = 565
        rows_per_page = 20  # Ajusta este valor según tu límite de filas por hoja
        for i, DetalleVenta in enumerate(queryset):
            if i % rows_per_page == 0 and i != 0:
                # Si alcanza el límite de filas por hoja, crea una nueva página
                p.showPage()
                logo_path = 'static/Iconos/icono_pdf.jpg'
                p.drawImage(logo_path, 50, 730, width=100, height=50)

                date_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                p.setFont("Helvetica", 8)
                p.drawRightString(600, 760, f"Generado el: {date_string}")

                # PDF Title
                p.setFont("Helvetica", 20)
                p.setFillColor(colors.darkblue)
                p.drawString(250, 750, "Factura")

                # Headers
                p.setFont("Helvetica", 12)
                p.setFillColor(colors.darkblue)
                p.drawString(70, 670, "ID Venta: ")
                p.drawString(350, 670, "Cliente: ")
                p.drawString(70, 650, "Fecha: ")
                p.drawString(350, 650, "Total: ")
                
                p.drawString(60, 600, " No ")
                p.drawString(100, 600, " PRODUCTO ")
                p.drawString(290, 600, " CANTIDAD ")
                p.drawString(470, 600, " SUBTOTAL ")
                p.setFillColor(colors.black)
                y_position = 565  # Reinicia la posición Y para la nueva página

        

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
