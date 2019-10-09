from . import views
from django.urls import path

app_name = 'cart'

urlpatterns = [      
    path('cart_view/', views.view_cart, name='view_cart'),
    path('cart_order/', views.cart_order, name='cart_order'),
    path('cart_link/<path:product_name>/', views.link_cart, name='link_cart'),
    path('cart_quantity/<path:product_names>/', views.plus_minus_quntity, name='plus_minus'),
    path('cart_remove/<path:product_names>/', views.remove_to_cart, name='cart_remove'),
]