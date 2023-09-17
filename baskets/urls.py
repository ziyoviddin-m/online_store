from django.urls import path

from . import views

app_name = 'baskets'

urlpatterns = [
    path('', views.basket, name='basket'),
    path('add/<int:product_id>/', views.basket_add, name='basket_add'),
    path('delete/<int:product_id>/', views.basket_remove, name='basket_remove'),
    path('delete/', views.basket_all_delete, name='basket_all_delete')
]