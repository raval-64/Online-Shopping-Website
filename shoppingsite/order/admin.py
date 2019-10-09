from django.contrib import admin
from .models import order_info, order, address_info

# Register your models here.
admin.site.register(address_info)
admin.site.register(order_info)
admin.site.register(order)

