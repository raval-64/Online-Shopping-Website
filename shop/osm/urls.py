from . import views
from django.urls import path
app_name = 'osm'

urlpatterns = [
    path('', views.index, name='index_main'),
    path('register/', views.register, name='register'),
    path('login_user/', views.login_user, name='login_user'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart_order/', views.cart_order, name='cart_order'),
    path('search/', views.search_found, name='search'),
    path('cart_link/<path:product_name>/', views.link_cart, name='link_cart'),
    path('cart_quantity/<path:product_names>/', views.plus_minus_quntity, name='plus_minus'),
    path('cart_remove/<path:product_names>/', views.remove_to_cart, name='cart_remove'),
    path('views/<str:product_types>/<path:product_name>/', views.product_detail, name='product_detail'),
    path('osm/<str:product_categorys>/<str:product_type_names>/', views.product_list, name='product_list'),
    path('osm/<str:product_brand_name>/', views.product_list_brand, name='product_list_brand'),
    path('buy/<path:product_names>/', views.order_buy, name='order_buy'),
    path('order/filladdress/', views.fill_address, name='fill_address'),
    path('order/payment/', views.payment_method, name='payment_method'),
    path('order/ordersummary/', views.order_summary, name='order_summary'),
    path('order-report/', views.report, name='order-report'),
    path('order-total-report/', views.total_report, name='total_report'),
]
