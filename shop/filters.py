import django_filters

from .models import ProductModel, OrderModel,PRODUCT_CHOICES,ORDER_CHOICES,AvailabilityModel
from django_filters import DateFilter, CharFilter, NumberFilter


class ProductFilter(django_filters.FilterSet):
    product_price_1 = NumberFilter(field_name='product_price', lookup_expr='gte')
    product_price_2 = NumberFilter(field_name='product_price', lookup_expr='lte')
    product_name = CharFilter(field_name='product_name', lookup_expr='icontains')
    materials = CharFilter(field_name='materials', lookup_expr='icontains')
    # product_type = NumberFilter(choices=PRODUCT_CHOICES)

    class Meta:
        model = ProductModel
        fields = "__all__"
        exclude = ['product_image']

class AvailabilityFilter(django_filters.FilterSet):
    store_names = CharFilter(field_name='store_name', lookup_expr='icontains')

    class Meta:
        model = AvailabilityModel
        fields = "__all__"
        exclude = ['product', 'store_name', 'number_of_available_items']

class OrderFilter(django_filters.FilterSet):
    date_of_order_pass = DateFilter(field_name='date_of_order', lookup_expr='gte')
    date_of_order_bef = DateFilter(field_name='date_of_order', lookup_expr='lte')
    total_price_1 = NumberFilter(field_name='price_of_order', lookup_expr='gte')
    total_price_2 = NumberFilter(field_name='price_of_order', lookup_expr='lte')
    address = CharFilter(field_name='address', lookup_expr='icontains')
    # order_type = NumberFilter(choices=ORDER_CHOICES)


    class Meta:
        model = OrderModel
        fields = ['product', 'date_of_order_pass','date_of_order_bef','total_price_1','total_price_2','address']
        exclude = ['amount','date_of_order','price_of_order']

# class OrderFilter2(django_filters.FilterSet):
#     date_of_order_pass = DateFilter(field_name='date_of_order', lookup_expr='gte')
#     date_of_order_bef = DateFilter(field_name='date_of_order', lookup_expr='lte')
#     total_price_1 = NumberFilter(field_name='price_of_order', lookup_expr='gte')
#     total_price_2 = NumberFilter(field_name='price_of_order', lookup_expr='lte')
#     address = CharFilter(field_name='address', lookup_expr='icontains')
#     # order_type = NumberFilter(choices=ORDER_CHOICES)
#
#
#     class Meta:
#         model = OrderModel
#         fields = "__all__"
#         exclude = ['amount','date_of_order','price_of_order','user','product']

#
# class CheckFilter(django_filters.FilterSet):
#     price_1 = NumberFilter(field_name='total_price', lookup_expr='gte')
#     price_2 = NumberFilter(field_name='total_price', lookup_expr='lte')
#
#     class Meta:
#         model = CheckModel
#         fields = "__all__"
#         exclude = ['user', 'order']

