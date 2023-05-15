# Django
from django.utils import timezone
from django.db import models
from django.db.models.fields.related import ForeignKey
from django.utils.translation import gettext_lazy as _

# Auth
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from .managers import AccountManager


class Usuarios(AbstractBaseUser, PermissionsMixin):
    """Modelo para la BD de una cuenta"""
    usuario = models.CharField(unique=True, max_length=80, null=False,
                               error_messages={
                                   "required": "Necesitas un nombre de usuario",
                                   'unique': "Este Usuario ya esta en uso",
                                   "max_length": "Tu nombre debe teer 80 caracteres máximo"
                               })
    nombre_1 = models.CharField(max_length=80,
                                error_messages={"required": "Necesitas escribir un nombre",
                                                "max_length": "Tu nombre debe teer 80 caracteres máximo"})
    nombre_2 = models.CharField(max_length=80, blank=True, null=False,
                                error_messages={"max_length": "Tu nombre debe teer 80 caracteres máximo"})
    apellido_p = models.CharField(max_length=110, null=False,
                                  error_messages={"required": "Necesitas escribir un apellido",
                                                  "max_length": "Tu apellido debe teer 110 caracteres máximo"})
    apellido_m = models.CharField(blank=True, max_length=110, null=False,
                                  error_messages={"max_length": "Tu apellido debe teer 110 caracteres máximo"})
    correo = models.EmailField(unique=True, max_length=150, null=False,
                               error_messages={'invalid': "Necesitas escribir un email valido",
                                               'unique': "Este email ya esta en uso",
                                               'required': 'Es necesario dar un email',
                                               "max_length": "Tu email solo puede tener 150 caracteres máximo"})
    # Datos de Usuarios para accion del administrador

    # Nota: el atributo ID de la entidad existe por defecto en Django

    # Perrmisos y auth
    TIPOS_DE_USUARIO = (
        (1, "Administrador"),
        (2, "Usuario_Nivel_1"),
        (3, "Usuario_Nivel_2"),
        (4, "Usuario_Nivel_3"),
        (5, "Usuario_Nivel_4"),
    )

    tipo = models.PositiveSmallIntegerField(choices=TIPOS_DE_USUARIO)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'usuario'
    REQUIRED_FIELDS = ['correo']
    objects = AccountManager()

    dependencia_origen = models.ForeignKey(
        'oficios.Dependencia', on_delete=models.CASCADE, default=0)

    def __str__(self):
        """Obtener represencacion como cadena"""
        if(self.nombre_2 == ''):
            return f"{self.usuario} | {self.nombre_1} {self.apellido_p} {self.apellido_m}"
        else:
            return f"{self.usuario} | {self.nombre_1} {self.nombre_2} {self.apellido_p} {self.apellido_m}"

    def __repr__(self):
        """Obtener represencacion como cadena"""
        return self.__str__()
