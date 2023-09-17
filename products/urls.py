from django.urls import path
from . import views
from products.views import *

app_name = 'products'

urlpatterns = [
    path('', ProductListView.as_view(), name='products'),
    path('<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/<int:category_id>/', ProductListView.as_view(), name='category'),

    path('search/', ProductListView.as_view(), name='search_products'),
    path('page/<int:page>/', ProductListView.as_view(), name='paginator'),

    path('favorites/', views.favorite, name='favorite'),
    path('favorites/add/<int:pk>/', views.favorite_add, name='favorite_add'),
    path('favorites/delete/<int:pk>/', views.favorite_delete, name='favorite_delete'),
    path('favorite/delete/', views.favorite_del_all, name='favorite_del_all'),
    
    path('contact/', ContactView.as_view(), name='contact'),
]