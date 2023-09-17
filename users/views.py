from django import http
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView, ListView

from common.mixin import TitleMixin
from products.models import *
from users.models import User, EmailVerification
from django.utils.timezone import now
from orders.models import Order

from .forms import *


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active and user.is_verified_email == True:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('home'))
            elif user.is_verified_email != True:
                messages.success(request, 'Пожалуйста подтвердите свой адрес электронной почты')
    else:
        form = UserLoginForm()

    context = {
        'form': form,
        'title': 'ZIYOVIDDIN - Авторизация'
    }
    return render(request, 'users/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('home'))


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    title = 'ZIYOVIDDIN - Регистрация'
    success_message = 'Для завершения процесса регистрации, пожалуйста, подтвердите свой адрес электронной почты! Загляните в почту!'


class UserProfileView(TitleMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'ZIYOVIDDIN - Профиль'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data()
        context['user'] = self.request.user
        context['orders'] = Order.objects.filter(initiator=self.request.user).order_by('-id')
        return context


class EmailVerificationView(TitleMixin, TemplateView):
    template_name = 'users/email_verification.html'
    title = 'ZIYOVIDDIN - Подтверждение эл. почты'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('home'))


    


# def register(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Вы успешно зарегестрировались!')
#             return HttpResponseRedirect(reverse('users:login'))
#     else:       
#         form = UserRegistrationForm()
#     categories = ProductCategory.objects.all()
#     context = {
#         'form': form,
#         'categories': categories,
#         'title': 'ZIYOVIDDIN - Регистрация'
#     }
#     return render(request, 'users/register.html', context)

# @login_required
# def profile(request):
#     if request.method == 'POST': 
#         form = UserProfileForm(instance=request.user, data=request.POST)
#         if form.is_valid():
#             form.save()
#             # update_session_auth_hash(request.user)
#             return HttpResponseRedirect(reverse('users:profile'))
#         else:
#             print(form.errors)
#     else:
#         form = UserProfileForm(instance=request.user)
#     categories = ProductCategory.objects.all()
#     context = {
#         'categories': categories,
#         'user': request.user,
#         'form': form,
#         'baskets': Basket.objects.filter(user=request.user),
#         'title': 'ZIYOVIDDIN - Профиль'
#     }
#     return render(request, 'users/profile.html', context)