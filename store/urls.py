from django.urls import path
from . import views

app_name = 'stores'

urlpatterns =[
    path('', views.store, name='store'),
    path('category/<slug:category_slug>/', views.store, name='product-by-category'),
    path('category/<slug:category_slug>/<slug:product_slug>', views.product_detail, name='product-detail'),
    path('search/', views.search, name='search'),
]