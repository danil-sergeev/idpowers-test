from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse_lazy

from tickets.models import Chat

# Create your tests here.

profile = get_user_model()


class ChatTestCase(TestCase):
    def setUp(self):
        self.customer = profile.objects.create(
            email='customer@customer.ru',
            password='12345'
        )
        self.admin = profile.objects.create(
            email='admin@admin.ru',
            password='12345'
        )
        self.outro_user = profile.objects.create(
            email='outro@outro.ru',
            password='12345'
        )
        self.chat = Chat.objects.create(
            admin=self.admin,
            customer=self.customer
        )
        self.client = Client(enforce_csrf_checks=True)

        self.chat_url = reverse_lazy('tickets:ticket', args={self.chat.pk})

    def test_detail_template(self):
        if self.client.login(email=self.customer.email,
                             password=self.customer.password):
            response = self.client.get(self.chat_url)
            message_form = response.context['form']
            self.assertTemplateUsed(response, template_name='chat/chat.html')
            self.assertContains(response, self.admin)
            self.assertContains(response, message_form)

    def test_access_with_outro_user(self):
        if self.client.login(email='outro@outro.ru',
                             password='12345'):
            response = self.client.get(self.chat_url)
            self.assertEqual(response.status_code, 404)

    def test_access_with_customer_user(self):
        if self.client.login(email=self.customer.email,
                             password=self.customer.password):
            response = self.client.get(self.chat_url)
            self.assertEqual(response.status_code, 200)

    def test_access_with_admin_user(self):
        if self.client.login(email=self.admin.email,
                             password=self.admin.password):
            response = self.client.get(self.chat_url)
            self.assertEqual(response.status_code, 200)

    def test_create_message_from_customer(self):
        if self.client.login(email=self.customer.email,
                             password=self.customer.password):
            response = self.client.post(self.chat_url,
                                        {"chat": self.chat, "sender": self.customer, "message": "test message"})
            self.assertEqual(response.status_code, 302)

    def test_create_message_from_admin(self):
        if self.client.login(email=self.admin.email,
                             password=self.admin.password):
            response = self.client.post(self.chat_url,
                                        {"chat": self.chat, "sender": self.admin, "message": "test message"})
            self.assertEqual(response.status_code, 302)
