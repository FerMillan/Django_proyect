from django.db import models
from django.conf import settings
from django.db.models.fields.related import ForeignKey
from datetime import datetime

from django.forms import DateTimeField

from django.utils.translation import gettext_lazy as _


class Oficio(models.Model):

    class Estatus(models.TextChoices):
        NUEVO = 'NU', _('Nuevo')
        NO_REVISADO = 'NR', _('No Revisado')
        LEIDO = 'L', _('Leido')
        SEGUIMIENTO = 'S', _('Seguimiento')
        COMPLETADO = 'C', _('Completado')
    
    class MES(models.TextChoices):
        ENERO = 'Ene',_('Enero')
        FEBRERO = 'Feb',_('Febrero')
        MARZO = 'Mar',_('Marzo')
        ABRIL = 'Abr',_('Abril')
        MAYO = 'May',_('Mayo')
        JUNIO = 'Jun',_('Junio')
        JULIO = 'Jul',_('Julio')
        AGOSTO = 'Ago',_('Agosto')
        SEPTIEMBRE = 'Sep',_('Septiembre')
        OCTUBRE = 'Oct',_('Octubre')
        NOVIEMBRE = 'Nov',_('Noviembre')
        DICIEMBRE = 'Dic',_('Diciembre')

    def mes_actual(MES):
        fecha = str(datetime.now().date())
        mes = int(fecha[5:7])

        if mes == 1:
            return MES.ENERO
        elif mes == 2:
            return MES.FEBRERO
        elif mes == 3:
            return MES.MARZO
        elif mes == 4:
            return MES.ABRIL
        elif mes == 5:
            return MES.MAYO
        elif mes == 6:
            return MES.JUNIO
        elif mes == 7:
            return MES.JULIO
        elif mes == 8:
            return MES.AGOSTO
        elif mes == 9:
            return MES.SEPTIEMBRE
        elif mes == 10:
            return MES.OCTUBRE
        elif mes == 11:
            return MES.NOVIEMBRE
        elif mes == 12:
            return MES.DICIEMBRE

    def año_actual():
        fecha = str(datetime.now().date())
        año = int(fecha[0:4])

        return año

    folio = models.CharField(
        primary_key=True, max_length=10, unique=True, null=False)
    usuario = ForeignKey('users.Usuarios', on_delete=models.PROTECT)
    # usuario = models.ForeignKey(
    #     settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='nombre_usuario')
    fecha = models.DateTimeField(auto_now_add=True)
    mes = models.CharField(
        max_length=3, choices=MES.choices, default=mes_actual(MES))
    año = models.IntegerField(error_messages={'required': 'Este campo es obligatorio'}, null=False, default=año_actual())
    asunto = models.TextField(null=False)
    estatus = models.CharField(
        max_length=2, choices=Estatus.choices, default=Estatus.NUEVO)
    documento = models.FileField(upload_to='static/pdf')
    dependencia = models.ForeignKey(
        'Dependencia', on_delete=models.CASCADE, related_name='dependencia_origen')
    turnado = models.ForeignKey(
        'Dependencia', on_delete=models.CASCADE, related_name='dependencia_destino')

    def __str__(self):
        return self.folio


class OficioRespuesta(models.Model):
    id_oficio_respuesta = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey('users.Usuarios', on_delete=models.CASCADE)
    id_oficio = models.ForeignKey(
        'Oficio', on_delete=models.CASCADE, related_name='folio_oficio')
    fecha = models.DateTimeField(auto_now_add=True)
    asunto = models.TextField(null=False)
    documento = models.FileField(upload_to='static/pdf')

    def __str__(self):
        return "Respuesta al folio: " + f'{self.id_oficio}'


class Dependencia(models.Model):
    id_dependencia = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    siglas = models.CharField(max_length=10, null=False)
    # usuario = ForeignKey('users.Usuarios', on_delete=models.PROTECT)
    # usuario = models.ForeignKey(
    #     settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def __str__(self):
        return self.siglas
