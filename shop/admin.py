from django.contrib import admin
from .models import ProductModel, OrderModel, ProductImageModel, AvailabilityModel,CheckModel
#
# Register your models here.
#
admin.site.register(ProductModel)
admin.site.register(OrderModel)
admin.site.register(CheckModel)
admin.site.register(ProductImageModel)
admin.site.register(AvailabilityModel)
#
