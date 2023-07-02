from django.db.models import QuerySet
from django_filters import rest_framework as filters
from .models import Client
from services.distance_service import find_min_max_latitude_longitude


class ClientFilter(filters.FilterSet):
    sex = filters.NumberFilter()
    first_name = filters.CharFilter(lookup_expr='icontains')
    last_name = filters.CharFilter(lookup_expr='icontains')
    distance = filters.NumberFilter(method='my_custom_filter')

    class Meta:
        model = Client
        fields = ['sex', 'first_name', 'last_name']

    def my_custom_filter(self, queryset: QuerySet, name: str, value: int) -> QuerySet:
        user = self.request.user
        distance = float(value / 1000)  # Перевод метров в км

        # Получение максимальных широты и долготы
        min_max_latitude_longitude = find_min_max_latitude_longitude(latitude=user.position_latitude,
                                                                     longitude=user.position_longitude,
                                                                     distance=distance)

        print(min_max_latitude_longitude)

        queryset = queryset.filter(position_latitude__lte=min_max_latitude_longitude['max_latitude'],
                                   position_latitude__gte=min_max_latitude_longitude['min_latitude'],
                                   position_longitude__lte=min_max_latitude_longitude['max_longitude'],
                                   position_longitude__gte=min_max_latitude_longitude['min_longitude'],
                                   )

        return queryset
