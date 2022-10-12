from django_filters import FilterSet, DateFromToRangeFilter
from advertisements.models import Advertisement


class AdvertisementFilter(FilterSet):
    """Фильтры для объявлений."""

    date = DateFromToRangeFilter(field_name='created_at')

    class Meta:
        model = Advertisement
        fields = ['date', 'creator', 'status']
