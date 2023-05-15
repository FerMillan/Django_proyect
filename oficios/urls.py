from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf.urls import url
from django.urls import path, include, re_path
from . import views
from django.views.generic.base import RedirectView

app_name = 'oficios'

urlpatterns = [
    path('', views.lista_oficios, name="list"),
    path('respuesta/', views.lista_oficios_respuesta, name="respuesta"),
    path('crear/', views.AgregarOficio.as_view(), name="crear"),
    path('editar_oficio/<str:pk>', views.editar_oficio, name="editar"),
    path('cambio_status/<str:pk>', views.change_status, name="status"),
    path('borrar_oficio/<str:pk>', views.borrar_oficio, name="borrar"),
    path('responder_oficio/<str:pk>', views.responder_oficio, name="responder"),
    path('dependencia/', views.agregar_dependencia, name="dependencia"),
    path('buscar/', views.buscar_oficio, name="buscar"),
]
