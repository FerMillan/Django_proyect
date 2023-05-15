from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf.urls import url
from django.urls import path, include
from . import views
from django.views.generic.base import RedirectView

app_name = 'reuniones'

urlpatterns = [
    path('', views.lista_reuniones, name='list'),
    path('calendario/semana', views.calendario_semana, name='semana'),
    path('calendario/2_semanas', views.calendario_2_semanas, name='2_semanas'),
    path('agregar/', views.AgregarReunion.as_view(), name='agregar'),
    path('borrar/<str:pk>', views.BorrarReunion.as_view(), name='borrar'),
    path('editar/<str:pk>', views.editar_reunion, name='editar'),
    path('agregar/participantes/<str:pk>', views.AgregarParticipante.as_view(), name='agregar_participantes'),
    path('participantes/<str:pk>', views.ParticipantesView.as_view(), name='participantes'),
    path('borrar/participantes/<str:fk>/<int:pk>', views.BorrarParticipante.as_view(), name='borrar_participantes'),
    path('editar/participantes/<str:fk>/<int:pk>', views.editar_participante, name='editar_participantes'),
    path('agregar/documento/<str:pk>', views.AgregarDocumento.as_view(), name='agregar_documento'),
    path('borrar/documento/<str:fk>/<int:pk>', views.BorrarDocumento.as_view(), name='borrar_documento'),
]
