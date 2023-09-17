from django.contrib.auth.decorators import login_required
from django.urls import path
from users.views import *

from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('profile/<int:pk>/', login_required(UserProfileView.as_view()), name='profile'),
    path('logout/', views.logout, name='logout'),
    path('verify/<str:email>/<uuid:code>/', EmailVerificationView.as_view(), name='email_verification'),
]