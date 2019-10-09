from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, RegexValidator

# Create your models here.
class seller_info(models.Model):
    seller_auth_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date_joined = models.DateField(blank=False)
    bank_acc_no = models.PositiveIntegerField(validators=[MaxValueValidator(999999999999999)])
    seller_shop_name = models.CharField(max_length=40, null=True)
    seller_shop_address = models.TextField(null=True)
    seller_shop_city = models.CharField(max_length=20, null=True)
    seller_shop_pincode = models.CharField(max_length=6, null=True, validators=[RegexValidator(r'^\d{6}$')])

    def __str__(self):
        return self.seller_shop_name

