from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order, name='order'),
    path('confirmacion', views.confirm, name="confirm"),
    path('cancelar', views.cancel, name="cancel"),
    path('confirm/', views.confirm_order, name='confirm_order'),
    # path('completar/', views.complete, name='complete'),
    path('completados/', views.OrderListView.as_view(), name='completeds'),
]
