import django_filters

from django_filters import DateFilter

from .models import Reunion


class BuscarReunion(django_filters.FilterSet):
    # start_date = DateFilter(field_name="fecha", lookup_expr="gte")
    # end_date = DateFilter(field_name="fecha", lookup_expr="lte")
    id = django_filters.CharFilter(label='Numero de oficio')

    class Meta:
        model = Reunion
        fields = ('id', 'fecha', 'mes', 'año','lugar', 'asunto')
