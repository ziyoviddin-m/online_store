from django.urls import path
from orders.views import *
from orders import views
from django.contrib.auth.decorators import login_required

app_name = 'orders'

urlpatterns = [
    path('order<int:pk>', login_required(OrderDetailView.as_view()), name='order'),
    path('order-create/', login_required(OrderCreateView.as_view()), name='order-create'),
    path('order-success/', login_required(SuccessTemplateView.as_view()), name='order-success'),
    path('success/', login_required(Success.as_view()), name='success'),
]