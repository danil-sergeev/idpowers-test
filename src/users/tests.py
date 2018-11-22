from django.test import TestCase, Client
from django.contrib.auth import get_user_model, authenticate
from django.urls import reverse_lazy
# Create your tests here.

profile = get_user_model()


class AuthTestCase(TestCase):
    def setUp(self):
        self.user = profile.objects.create(
            email='test@test.ru',
            password='12345'
        )
        self.client = Client()

    def test_authenticate(self):
        auth = authenticate(email=self.user.email, password=self.user.password)
        self.assertTrue(auth)

    def test_signup(self):
        signup_url = reverse_lazy('users:sign-up')
        response = self.client.post(signup_url, {"email": "test@test.com", "password": '54321'})
        self.assertEqual(response.status_code, 302)

    def test_login_view(self):
        login_url = reverse_lazy('users:login')
        response = self.client.post(login_url, {"email": self.user.email, "password": self.user.password})
        self.assertEqual(response.status_code, 302)
