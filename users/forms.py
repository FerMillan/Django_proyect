from django import forms
from django.forms import Form

# Auth
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate

# Models

from .models import Usuarios


class CreateUsuarioForm(UserCreationForm):
    """Define un formulario para crear Cliente"""

    def clean_username(self):
        # Desde que Usuarios.usuario es único, esta revision es redundante
        # pero es un mensaje mas personalizado que el que viene por defecto.
        username = self.cleaned_data["usuario"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['Ya existe una cuenta con este usuario'])

    def clean_email(self):
        # Desde que Usuarios.correo es único, esta revision es redundante
        # pero es un mensaje mas personalizado que el que viene por defecto.
        email = self.cleaned_data["correo"]
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(
            self.error_messages['Ya existe una cuenta con este correo'])

    class Meta(UserCreationForm):
        model = Usuarios
        fields = ['usuario', 'nombre_1', 'nombre_2',
                  'apellido_p', 'apellido_m', 'correo', ]
        labels = {
            'nombre_1': ('Nombre'),
            'nombre_2': ('Segundo Nombre *'),
            'apellido_p': ('Apellido Paterno'),
            'apellido_m': ('Apellido Materno*'),
            'correo': ('Correo Electrónico'),
        }


class UpdateUsuarioForm(forms.ModelForm):
    """Define un formulario para modificar una cuenta"""
    class Meta:
        model = Usuarios
        fields = ['nombre_1', 'nombre_2',
                  'apellido_p', 'apellido_m', 'correo', 'dependencia_origen', ]
        exclude = ['password', ]
        labels = {
            'nombre_1': ('Nombre'),
            'nombre_2': ('Segundo Nombre *'),
            'apellido_p': ('Apellido Paterno'),
            'apellido_m': ('Apellido Materno'),
            'correo': ('Correo Electrónico'),
        }


class UsuarioLoginForm(Form):
    """Define un formulario para iniciar sesión"""
    username = forms.CharField(max_length=150,
                               # help_text='Escribe un usuario adecuado',
                               error_messages={'invalid': "Necesitas escribir un usuario valido",
                                               'required': 'Es necesario llenar este campo',
                                               "max_length": "El usuario solo puede tener 80 caracteres máximo"})
    password = forms.CharField()
    labels = {
        'username': ('Usuario'),
        'password': ('Contraseña'),
    }
