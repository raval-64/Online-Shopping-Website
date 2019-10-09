from django.contrib import admin
from .models import product_category,product, product_type, product_gallery
# Register your models here.
admin.site.register(product_category)
admin.site.register(product_type)
admin.site.register(product)
admin.site.register(product_gallery)
