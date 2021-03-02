''' Importing Views '''
from . import views
from django.urls import path

app_name = 'products'

urlpatterns = [
    path('', views.index, name='index'),
    path('view-detail/<str:product_types>/<path:product_name>/', views.product_view_detail, name='product_detail'),
    path('view-list/<str:product_categories>/<str:product_type_names>/', views.product_view_list, name='product_list'),
    path('view-brand/<str:product_brand_name>/', views.product_view_list_by_brand, name='product_list_brand'),
    path('search/', views.search, name='search'),
]