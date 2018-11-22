from django.test import TestCase, Client
from django.urls import reverse_lazy

from posts.models import Post, Comment, Mark, Category
from users.models import Profile


# Create your tests here.


class PostDetailViewTestCase(TestCase):

    def setUp(self):
        self.author = Profile.objects.create(
            email='test123@test.ru',
            password='12345'
        )
        self.category = Category.objects.create(
            title='Test Category'
        )
        self.post = Post.objects.create(
            author=self.author,
            category=self.category,
            title='Test title',
            summary='Test summary',
            content='Test content'
        )
        self.detail_url = reverse_lazy('posts:detail-post', args={self.post.pk})

    def test_detail_template(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='post_detail.html')

    def test_detail_template_fields(self):
        response = self.client.get(self.detail_url)
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.content)


class NotAuthorPostTestCase(TestCase):

    def setUp(self):
        self.author = Profile.objects.create(
            email='test123@test.ru',
            password='12345'
        )
        self.customer = Profile.objects.create(
            email='customer@test.ru',
            password='12345'
        )

        self.client = Client(enforce_csrf_checks=True)

        self.category = Category.objects.create(
            title='Test Category'
        )
        self.post = Post.objects.create(
            author=self.author,
            category=self.category,
            title='Test title',
            summary='Test summary',
            content='Test content'
        )
        self.detail_url = reverse_lazy('posts:detail-post', args={self.post.pk})
        self.delete_url = reverse_lazy("posts:delete", args={self.post.pk})
        self.edit_url = reverse_lazy("posts:edit", args={self.post.pk})

    def test_template(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="post_detail.html")
        self.assertContains(response, self.post.author.email)

    def test_comment_context(self):
        if self.client.login(email=self.customer.email,
                             password=self.customer.password):
            response = self.client.get(self.detail_url)
            comment_form = response.context['form']
            self.assertContains(response, comment_form)

    def test_delete_post_access(self):
        if self.client.login(email=self.customer.email,
                             password=self.customer.password):
            response = self.client.post(self.delete_url)
            self.assertEqual(response.status_code, 404)

    def test_edit_post_access(self):
        if self.client.login(email=self.customer.email,
                             password=self.customer.password):
            response = self.client.post(self.edit_url)
            self.assertEqual(response.status_code, 404)

    def test_can_comment(self):
        if self.client.login(email=self.customer.email,
                             password=self.customer.password):
            response = self.client.post(self.detail_url,
                                        {"content": "Test comment", "post": self.post, "sender": self.customer})
            self.assertEqual(response.status_code, 302)

    def test_can_mark(self):
        if self.client.login(email=self.customer.email,
                             password=self.customer.password):
            response = self.client.post(self.detail_url, {"mark": 5, "post": self.post, "sender": self.customer})
            self.assertEqual(response.status_code, 302)


