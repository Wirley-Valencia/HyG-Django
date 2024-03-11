"""
URL configuration for proyectohyg project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
# Media files
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from products.views import ProductListView
from django.urls import include


urlpatterns = [
    path('orden/', include('orders.urls')),
    path('carrito/', include('carts.urls')),
    path('productos/', include('products.urls')),
    path('catalogo/', ProductListView.as_view(), name='catalogo'),
    path('admin/', admin.site.urls, name='admin:index'),
    path('', views.inicio, name='inicio'),
    path('contacto/', views.contacto, name='contacto'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('dashboardAdmin/', views.dashboard_administrador,
         name='dashboard_administrador'),
    path('dashboardClient/', views.dashboard_cliente, name='dashboard_cliente'),
    path('login', views.login_view, name='login'),
    path('registro/', views.registro, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    path('rContraseña/', views.rContraseña, name='rContraseña'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='plantillalogin.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(
        template_name='anuncioR.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='nuevaC.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='contraseñaC.html'), name='password_reset_complete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
