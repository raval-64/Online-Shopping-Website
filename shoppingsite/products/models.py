from django.db import models
from seller.models import seller_info
from django.core.validators import RegexValidator
# Create your models here.

class product_category(models.Model):
    product_category_name = models.CharField(max_length=20)

    def __str__(self):
        return self.product_category_name

class product_type(models.Model):
    product_type_name = models.CharField(max_length=30)
    product_category_id = models.ForeignKey(product_category, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_type_name

class product(models.Model):
    product_name = models.CharField(max_length=60)
    product_type_id = models.ForeignKey(product_type, on_delete=models.CASCADE)
    seller_id = models.ForeignKey(seller_info, on_delete=models.CASCADE)
    product_price = models.FloatField()
    product_desc = models.TextField()
    product_quantity = models.IntegerField(validators=[RegexValidator(r'^\d[0-9]*$')])
    product_brand = models.CharField(max_length=15)
    product_add_date = models.DateField(blank=False)

    def __str__(self):
        return self.product_name


class product_gallery(models.Model):
    gallery_name = models.FileField()
    gallery_type = models.CharField(max_length=10)
    product_id = models.ForeignKey(product, on_delete=models.CASCADE)

