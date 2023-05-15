from django.contrib import admin
from .models import Oficio, Dependencia, OficioRespuesta

# Register your models here.
admin.site.register(Oficio)
admin.site.register(Dependencia)
admin.site.register(OficioRespuesta)
