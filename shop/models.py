from django.db import models
import django.contrib.auth
from django.urls import reverse

# Create your models here.
PRODUCT_CHOICES = [
    (1, 'Ring'),
    (2, 'Earrings'),
    (3, 'Neklace'),
    (4, 'Bracelet'),
    (5, 'Charm'),
    (6, 'Clip'),
]
ORDER_CHOICES = [
    (1, 'Gift'),
    (2, 'Purchase'),

]

class ProductModel(models.Model):
    product_name = models.CharField(max_length=255, blank=False)
    product_price = models.DecimalField(decimal_places=2, max_digits=10)
    materials = models.TextField(default="")
    product_image = models.ImageField(upload_to='products')
    product_type = models.IntegerField(choices=PRODUCT_CHOICES)

    def __str__(self):
        return str(self.product_name) + " " + str(self.product_type)
    def get_absolute_url(self):
        return reverse('product-detail', args=[str(self.id)])




class OrderModel(models.Model):
    user = models.ForeignKey(django.contrib.auth.get_user_model(), null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, null=False, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=False)
    order_type = models.IntegerField(choices=ORDER_CHOICES)
    amount = models.IntegerField()
    date_of_order = models.DateField(auto_now_add=True)
    price_of_order = models.DecimalField(decimal_places=2, max_digits=10)


    def get_absolute_url(self):
        return reverse('order-detail', args=[str(self.id)])

    def __str__(self):
        return str(self.product) + "on date:"+str(self.date_of_order.strftime('%d.%m.%Y'))+" amount of order: "+str(self.amount)+", " + str(self.price_of_order) + " eur. "


class ProductImageModel(models.Model):
    hotel = models.ForeignKey(ProductModel, null=False, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/product')


class CheckModel(models.Model):
    user = models.ForeignKey(django.contrib.auth.get_user_model(), null=True, on_delete=models.CASCADE)
    order = models.ForeignKey(OrderModel, null=False, on_delete=models.CASCADE)
    # check_date = models.DateField(auto_now_add=True)
    total_price = models.DecimalField(decimal_places=2, max_digits=10, null=True)

    def get_absolute_url(self):
        return reverse('check-detail', args=[str(self.id)])

    def __str__(self):
        return str(self.order) + "total sum of: "+ str(self.total_price)
               # + ", on  " + str(self.check_date.strftime('%d.%m.%Y'))


