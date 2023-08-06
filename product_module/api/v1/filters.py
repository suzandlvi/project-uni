from django.db.models import Q
from django_filters.rest_framework import FilterSet, filters

from product_module.models import Product


class ProductFilter(FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")
    category = filters.CharFilter(field_name="category__title", method="filter_category")
    brand = filters.CharFilter(field_name="brand__title", method="filter_brand")
    title = filters.CharFilter(field_name="title", lookup_expr="contains")
    quantity = filters.BooleanFilter(field_name='quantity', method='filter_quantity')
    search = filters.CharFilter(method='my_custom_filter', label="search")

    def my_custom_filter(self, queryset, name, value):
        if value:
            return queryset.filter(Q(title__contains=value) |
                                   Q(brand__english_title__contains=value) |
                                   Q(brand__title__contains=value) |
                                   Q(category__title__contains=value)
                                   )
        return queryset

    def filter_quantity(self, queryset, name, value):
        # construct the full lookup expression.
        # print(name)
        # print(value)
        if value:
            return queryset.filter(quantity__gte=1)
        else:
            return queryset

    def filter_category(self, queryset, name, value):
        if value:
            return queryset.filter(category__title__exact=value)
        return queryset

    def filter_brand(self, queryset, name, value):
        if value:
            return queryset.filter(brand__title__exact=value)
        return queryset

    # alternatively, you could opt to hardcode the lookup. e.g.,
    # return queryset.filter(published_on__isnull=False)

    class Meta:
        model = Product
        fields = ["title", "min_price", "max_price", "quantity", "category", "brand"]
