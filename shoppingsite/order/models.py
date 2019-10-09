from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, RegexValidator
from products.models import product

# Create your models here.
class address_info(models.Model):
    name = models.CharField(max_length=20)
    mobile_no = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{10}$')])
    address = models.TextField()
    pincode = models.CharField(max_length=6, validators=[RegexValidator(r'^\d{6}$')])
    city = models.CharField(max_length=10)
    state = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class order_info(models.Model):
    order_date = models.DateField()
    order_payment_method = models.CharField(max_length=15)
    order_quantity = models.IntegerField(validators=[RegexValidator(r'^\d[0-9]*$')])
    order_total_payment = models.FloatField(max_length=20)
    order_delivery_date = models.DateField()

    def __str__(self):
        return self.order_payment_method


class order(models.Model):
    order_product_id = models.ForeignKey(product, on_delete=models.CASCADE)
    order_auth_id = models.ForeignKey(User, on_delete=models.CASCADE)
    order_address_id = models.ForeignKey(address_info, on_delete=models.CASCADE)
    order_info_id = models.ForeignKey(order_info, on_delete=models.CASCADE)
