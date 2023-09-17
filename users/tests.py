from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now
from datetime import timedelta

from users.models import User, EmailVerification

class UserRegistrationViewTestCase(TestCase):
    
    def setUp(self):
        self.data = {
            'first_name': 'Aleksey', 'last_name': 'Pavlov',
            'username': 'aleks', 'email': 'aleks@gmail.com',
            'password1': '12345678pP', 'password2': '12345678pP',
        }
        self.url = reverse('users:register')

    def test_user_registration_get(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'ZIYOVIDDIN - Регистрация')
        self.assertTemplateUsed(response, 'users/register.html')

    def test_user_registration_post_succes(self):
        username = self.data['username']
        self.assertFalse(User.objects.filter(username=username).exists())
        response = self.client.post(self.url, self.data)

        # check creating of user
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.filter(username=username).exists())

        # chek creating of email verification
        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verification.exists())
        self.assertEqual(
            email_verification.first().expiration.date(),
            (now() + timedelta(hours=48)).date()
        )
