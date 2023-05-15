from django.db import models
from django.db.models.fields.related import ForeignKey
from datetime import datetime

from django.utils.translation import gettext_lazy as _

class Reunion(models.Model):

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
    

    folio = models.CharField(primary_key=True, max_length=10, unique=True, null=False, blank=False)
    fecha = models.DateField(
        error_messages={'required': 'Este campo es obligatorio'}, null=False)
    mes = models.CharField(
        max_length=3, choices=MES.choices, default=mes_actual(MES))
    año = models.IntegerField(error_messages={'required': 'Este campo es obligatorio'}, null=False, default=año_actual())
    inicio = models.TimeField(
        error_messages={'required': 'Este campo es obligatorio'})
    termino = models.TimeField(
        error_messages={'required': 'Este campo es obligatorio'})
    lugar = models.TextField(max_length=180, error_messages={
                             'required': 'Este campo es obligatorio'})
    asunto = models.CharField(max_length=120, error_messages={
                              'required': 'Este campo es obligatorio', "max_length": "La longitud máxima es de 120 caracteres"})
    observaciones = models.TextField(max_length=200, error_messages={
                                     'required': 'Este campo es obligatorio'})

    usuario = ForeignKey('users.Usuarios', on_delete=models.PROTECT)

    """ Metodos de clase """

    def __str__(self):
        """Obtener represencacion como cadena"""
        return f"{self.fecha} \n {self.inicio} \n {self.termino} \n \n {self.lugar} \n \n {self.asunto} \n {self.observaciones}"

    def __repr__(self):
        """Obtener represencacion como cadena"""
        return self.__str__()


class Participante(models.Model):
    nombre = models.CharField(max_length=80, help_text='Nombre', error_messages={
                              'required': 'Este campo es obligatorio', "max_length": "La longitud máxima es de 80 caracteres"})
    apellido_p = models.CharField(max_length=80, help_text='Apellido Paterno', error_messages={
                                  'required': 'Este campo es obligatorio', "max_length": "La longitud máxima es de 80 caracteres"})
    apellido_m = models.CharField(max_length=80, help_text='Apellido Materno', error_messages={
                                  'required': 'Este campo es obligatorio', "max_length": "La longitud máxima es de 80 caracteres"})
    instituto = models.CharField(max_length=200, help_text='Instituto', error_messages={
                                 'required': 'Este campo es obligatorio', "max_length": "La longitud máxima es de 200 caracteres"})
    email = models.EmailField(
        error_messages={'required': 'Este campo es obligatorio'})

    """ Relaciones """

    reunion = models.ForeignKey(Reunion, on_delete=models.CASCADE)

    def __str__(self):
        """Obtener represencacion como cadena"""
        return f"{self.nombre} \n {self.apellido_p} \n {self.apellido_m} \n \n {self.instituto} \n \n {self.email} \n \n {self.reunion} "

    def __repr__(self):
        """Obtener represencacion como cadena"""
        return self.__str__()


class Documento(models.Model):
    documento = models.FileField(upload_to='static/pdf', blank=True)

    reunion = models.ForeignKey(Reunion, on_delete=models.CASCADE)

    def __str__(self):
        """Obtener represencacion como cadena"""
        return f"{self.documento}"

    def __repr__(self):
        """Obtener represencacion como cadena"""
        return self.__str__()
