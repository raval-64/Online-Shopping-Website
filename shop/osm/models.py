from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, RegexValidator
# Create your models here.


class mobile_detail(models.Model):
    m_id = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile_no = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{10}$')])

    def __str__(self):
        return self.mobile_no


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


class product_category(models.Model):
    product_category_name = models.CharField(max_length=20)

    def __str__(self):
        return self.product_category_name


class product_type(models.Model):
    product_type_name = models.CharField(max_length=20)
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


class cart(models.Model):
    cart_product_id = models.ForeignKey(product, on_delete=models.CASCADE)
    cart_auth_id = models.ForeignKey(User, on_delete=models.CASCADE)
    cart_quantity = models.IntegerField(validators=[RegexValidator(r'^\d[0-9]*$')], default=1)
    check = models.BooleanField('avilable', default=True)


class feedback(models.Model):
    feedback_name = models.CharField(max_length=15)
    feedback_email = models.EmailField()
    feedback_type = models.CharField(max_length=15)
    feedback_desc = models.TextField()
    feedback_auth_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.feedback_name
