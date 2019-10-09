from . import views
from django.urls import path

app_name = 'order'

urlpatterns = [
    path('buy/<path:product_names>/', views.order_buy, name='order_buy'),
    path('order/filladdress/', views.fill_address, name='fill_address'),
    path('order/payment/', views.payment_method, name='payment_method'),
    path('order/ordersummary/', views.order_summary, name='order_summary'),
    path('order-report/', views.report, name='order-report'),
    path('order-total-report/', views.total_report, name='total_report'),
]