from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, RegexValidator
from products.models import product

# Create your models here.
class cart(models.Model):
    cart_product_id = models.ForeignKey(product, on_delete=models.CASCADE)
    cart_auth_id = models.ForeignKey(User, on_delete=models.CASCADE)
    cart_quantity = models.IntegerField(validators=[RegexValidator(r'^\d[0-9]*$')], default=1)
    check = models.BooleanField('available', default=True)
