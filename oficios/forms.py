from django import forms
from . import models


class CreateOficio(forms.ModelForm):

    class Meta:
        model = models.Oficio
        fields = ['folio', 'dependencia', 'turnado',
                  'asunto', 'estatus', 'documento']
        labels = {'folio': 'Número de registro'}
        # widgets = {
        #     'myfield': forms.TextInput(attrs={'class': 'input-group input-group-lg'}),
        # }


class CreateOficioDeRespuesta(forms.ModelForm):

    class Meta:
        model = models.OficioRespuesta
        fields = ['asunto', 'documento']

# 'id_oficio', 
class UpdateOficio(forms.ModelForm):
    class Meta:
        model = models.Oficio
        fields = ['dependencia', 'turnado',
                  'asunto', 'estatus', 'documento']


class UpdateStatus(forms.ModelForm):

    class Meta:
        model = models.Oficio
        fields = ['estatus']


class CreateDependency(forms.ModelForm):
    class Meta:
        model = models.Dependencia
        fields = ['nombre', 'siglas']
