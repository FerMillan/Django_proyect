from django.urls import path

from . import views

app_name = 'usuario'

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name="signup"),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('perfil/<int:pk>', views.perfil, name="perfil"),
    #path('editar_perfil/<str:pk>', views.EditarPerfil.as_view(), name="editar"),
    path('editar_perfil/<str:pk>', views.editar_perfil, name="editar"),
    path('crear/<str:pk>', views.crear_perfil, name="crear"),
    #path('', views.index, name='index'),
]