
from django_filters import rest_framework as filters
from .models import Merchant


class MerchantFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    created_at = filters.DateFromToRangeFilter()

    class Meta:
        model = Merchant
        fields = ['id', 'integrate_facebook', 'is_published', 'is_active', 'created_at']
