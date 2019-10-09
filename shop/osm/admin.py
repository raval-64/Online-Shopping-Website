from django.contrib import admin
from .models import mobile_detail, order_info, order, seller_info, address_info, feedback, product_category, cart, product, product_type, product_gallery
# Register your models here.
admin.site.register(mobile_detail)
admin.site.register(seller_info)
admin.site.register(product_category)
admin.site.register(product_type)
admin.site.register(product)
admin.site.register(product_gallery)
admin.site.register(address_info)
admin.site.register(order_info)
admin.site.register(order)
admin.site.register(cart)
admin.site.register(feedback)
