import django_filters
from django_filters import DateFilter

from .models import *


class OrderFilter(django_filters.FilterSet):
    folio = django_filters.CharFilter(label='Numero de registro')

    class Meta:
        model = Oficio
        fields = ['folio', 'fecha', 'mes', 'año', 'usuario', 'dependencia', 'turnado',
                  'asunto', 'estatus']


class OrderFilterRespuesta(django_filters.FilterSet):

    # date = DateFilter(field_name="fecha", lookup_expr='gte')

    class Meta:
        model = OficioRespuesta
        fields = ['id_usuario', 'fecha', 'id_oficio',
                  'asunto']
