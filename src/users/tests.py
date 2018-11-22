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

    def test_signup(self):
        signup_url = reverse_lazy('users:sign-up')
        response = self.client.post(signup_url, {"email": "test@test.com", "password": '54321'})
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        login_url = reverse_lazy('users:login')
        response = self.client.post(login_url, {"email": self.user.email, "password": self.user.password})
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        logout_url = reverse_lazy('users:logout')
        if self.client.login(email=self.user.email, password=self.user.password):
            response = self.client.get(logout_url)
            self.assertEqual(response.status_code, 200)


class ProfileDetailView(TestCase):
    def setUp(self):
        self.user = profile.objects.create(
            email='test@test.ru',
            password='12345'
        )
        self.another_user = profile.objects.create(
            email='test2@test.ru',
            password='54321'
        )
        self.client = Client(enforce_csrf_checks=True)
        self.detail_url = reverse_lazy("users:detail", args={self.user.pk})
        self.edit_url = reverse_lazy('users:edit', args={self.user.pk})

    def test_template(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='profile/profile_detail.html')
        self.assertContains(response, self.user.email)

    def test_update_view(self):
        if self.client.login(email=self.user.email, password=self.user.password):
            response = self.client.post(self.edit_url,
                                        {"skype": 'yungcatx', "telephone": '+79826483305', 'first_name': 'Daniel',
                                         'last_name': 'Sergeev'})
            self.assertEqual(response.status_code, 302)

    def test_update_access(self):
        if self.client.login(email=self.another_user.email, password=self.another_user.password):
            response = self.client.post(self.edit_url,
                                        {"skype": 'yungcatx', "telephone": '+79826483305', 'first_name': 'Daniel',
                                         'last_name': 'Sergeev'})
            self.assertEqual(response.status_code, 404)
