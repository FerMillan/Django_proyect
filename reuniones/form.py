from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.forms.widgets import DateInput, Widget

from datetime import datetime

from reuniones.models import Documento, Reunion
from reuniones.models import Participante

from django.db import models

class ReunionForm(forms.ModelForm):
    class Meta:
        model = Reunion
        fields = ('folio','fecha','inicio','termino','lugar','asunto','observaciones')
        labels = {
            'folio': ('Número de Reunión'),
            'fecha': ('Fecha de Reunión'),
            'inicio': ('Hora de inicio de la Reunión'),
            'termino' : ('Hora de termino de la Reunión'),
            'lugar' : ('Lugar de Reunión'),
            'asunto': ('Asunto de la Reunión'),
            'observaciones': ('Observaciones')
        }
        error_messages = {
            'folio': {
                'required': ("Campo obligatorio, Favor de llenar"),
            },
            'fecha': {
                'required': ("Campo obligatorio, Favor de llenar"),
            },
            'inicio': {
                'required': ("Campo obligatorio, Favor de llenar"),
            },
            'termino': {
                'required': ("Campo obligatorio, Favor de llenar"),
            },
            'lugar': {
                'required': ("Campo obligatorio, Favor de llenar"),
            },
            'asunto': {
                'required': ("Campo obligatorio, Favor de llenar"),
            },
            'observaciones': {
                'required': ("Campo obligatorio, Favor de llenar"),
            },
        }

    def clean_asunto(self):
        data = self.cleaned_data.get("asunto")
        ini = self.cleaned_data.get("inicio")
        fin = self.cleaned_data.get("termino")
        mfecha = self.cleaned_data.get("fecha")

        fecha = str(datetime.now().date())
        año = int(fecha[0:4])
        mes = int(fecha[5:7])
        dia = int(fecha[8:10])
        hora = str(datetime.now().time())

        print(hora[0:8])
        print(str(ini))

        if ini == fin:
            raise forms.ValidationError("Las horas no pueden ser iguales")

        if (dia == int(str(mfecha)[8:10]) and mes == int(str(mfecha)[5:7])) and hora > str(ini): 
            raise forms.ValidationError("La hora de Inicio de Reunión no puede ser menor que la actual")
        elif int(str(ini)[0:2]) > int(str(fin)[0:2]):
            raise forms.ValidationError(f"La hora de Inicio no puede ser Mayor que la de Termino")
        elif int(str(ini)[0:2]) == int(str(fin)[0:2]) and int(str(ini)[3:5]) > int(str(fin)[3:5]):
            raise forms.ValidationError(f"La hora de Inicio no puede ser Mayor que la de Termino")
        elif int(str(ini)[0:2]) == 00 and int(str(fin)[0:2]) == 23:
            raise forms.ValidationError(f"La hora de Inicio no puede ser Mayor que la de Termino")
        

        if año > int(str(mfecha)[0:4]):
            raise forms.ValidationError(f"El Año de Reunión no puede ser anterior del actual")
        elif año == int(str(mfecha)[0:4]) and mes > int(str(mfecha)[5:7]):
            raise forms.ValidationError(f"El Mes de Reunión no puede ser anterior del actual en el año en curso")
        elif año == int(str(mfecha)[0:4]) and mes == int(str(mfecha)[5:7]) and dia-1 > int(str(mfecha)[8:10]):
            raise forms.ValidationError(f"El Día de Reunión no puede ser anterior del actual")

        # if Reunion.objects.filter(asunto=data).count() > 0:
        #     raise forms.ValidationError(f"Reunion existente con el asunto: \"{data}\"")

        return data

class ReunionFormUpdate(forms.ModelForm):
    class Meta:
        model = Reunion
        fields = ('fecha','inicio','termino','lugar','asunto','observaciones')
        labels = {
            'fecha': ('Fecha de Reunión'),
            'inicio': ('Hora de inicio de la Reunión'),
            'termino' : ('Hora de termino de la Reunión'),
            'lugar' : ('Lugar de Reunión'),
            'asunto': ('Asunto de la Reunión'),
            'observaciones': ('Observaciones')
        }
        error_messages = {
            'fecha': {
                'required': ("Campo obligatorio, Favor de llenar"),
            },
            'inicio': {
                'required': ("Campo obligatorio, Favor de llenar"),
            },
            'termino': {
                'required': ("Campo obligatorio, Favor de llenar"),
            },
            'lugar': {
                'required': ("Campo obligatorio, Favor de llenar"),
            },
            'asunto': {
                'required': ("Campo obligatorio, Favor de llenar"),
            },
            'observaciones': {
                'required': ("Campo obligatorio, Favor de llenar"),
            },
        }

    def clean_asunto(self):
        data = self.cleaned_data.get("asunto")
        ini = self.cleaned_data.get("inicio")
        fin = self.cleaned_data.get("termino")
        mfecha = self.cleaned_data.get("fecha")

        fecha = str(datetime.now().date())
        año = int(fecha[0:4])
        mes = int(fecha[5:7])
        dia = int(fecha[8:10])
        hora = str(datetime.now().time())

        print(hora[0:8])
        print(str(ini))

        if ini == fin:
            raise forms.ValidationError("Las horas no pueden ser iguales")

        if (dia == int(str(mfecha)[8:10]) and mes == int(str(mfecha)[5:7])) and hora > str(ini): 
            raise forms.ValidationError("La hora de Inicio de Reunión no puede ser menor que la actual")
        elif int(str(ini)[0:2]) > int(str(fin)[0:2]):
            raise forms.ValidationError(f"La hora de Inicio no puede ser Mayor que la de Termino")
        elif int(str(ini)[0:2]) == int(str(fin)[0:2]) and int(str(ini)[3:5]) > int(str(fin)[3:5]):
            raise forms.ValidationError(f"La hora de Inicio no puede ser Mayor que la de Termino")
        elif int(str(ini)[0:2]) == 00 and int(str(fin)[0:2]) == 23:
            raise forms.ValidationError(f"La hora de Inicio no puede ser Mayor que la de Termino")
        

        if año > int(str(mfecha)[0:4]):
            raise forms.ValidationError(f"El Año de Reunión no puede ser anterior del actual")
        elif año == int(str(mfecha)[0:4]) and mes > int(str(mfecha)[5:7]):
            raise forms.ValidationError(f"El Mes de Reunión no puede ser anterior del actual en el año en curso")
        elif año == int(str(mfecha)[0:4]) and mes == int(str(mfecha)[5:7]) and dia-1 > int(str(mfecha)[8:10]):
            raise forms.ValidationError(f"El Día de Reunión no puede ser anterior del actual")

        # if Reunion.objects.filter(asunto=data).count() > 0:
        #     raise forms.ValidationError(f"Reunion existente con el asunto: \"{data}\"")

        return data

class ParticipanteForm(forms.ModelForm):
    class Meta:
        model = Participante
        fields = ('nombre','apellido_p','apellido_m','instituto','email',)
        labels = {
            'nombre': ('Nombre (S)'),
            'apellido_p': ('Apellido Paterno'),
            'apellido_m' : ('Apellido Materno'),
            'instituto' : ('Institucion de Procedencia'),
            'email': ('Correo Electrónico'),
        }
        error_messages = {
            'nombre': {
                'required': ("Campo obligatorio, Favor de llenar"),
            },
            'apellido_p': {
                'required': ("Campo obligatorio, Favor de llenar"),
            },
            'apellido_m': {
                'required': ("Campo obligatorio, Favor de llenar"),
            },
            'instituto': {
                'required': ("Campo obligatorio, Favor de llenar"),
            },
            'email': {
                'required': ("Campo obligatorio, Favor de llenar"),
            },
        }

class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ('documento',)
        labels = {
            'documento': ('Archivo'),
        }

    # def clean_email(self):
    #     data = self.cleaned_data.get("email")

    #     if Participante.objects.filter(email=data).count() > 0:
    #         raise forms.ValidationError("Participante Agregado previamente con ese correo")

    #     return data