from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

class AuthenticationTest(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_login(self):
        # Проверяем, что страница входа доступна
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

        # Вводим правильные учетные данные и проверяем, что пользователь вошел
        response = self.client.post(reverse('login'), {'username': self.username, 'password': self.password})
        self.assertRedirects(response, reverse('home'))
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_logout(self):
        # Логинимся, чтобы выполнить проверку выхода
        self.client.login(username=self.username, password=self.password)

        # Проверяем, что пользователь вошел
        self.assertTrue('_auth_user_id' in self.client.session)

        # Выходим и проверяем, что пользователь вышел
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_unauthorized_access(self):
        # Проверяем, что неавторизованные пользователи не могут получить доступ к защищенным страницам
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('home'))
