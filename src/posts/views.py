from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.urls import reverse_lazy
from django.views import generic

from posts.models import Post, Category
from posts.forms import PostForm


# Create your views here.

class PostsByCategory(generic.ListView):
    template_name = 'posts.html'

    def get_queryset(self):
        title = self.kwargs['title']
        queryset = Category.objects.prefetch_related(
            Prefetch('posts_by_category')
        ).filter(title__iexact=self.title)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        title = self.kwargs['title']
        context = super(GetPostsByCategory, self).get_context_data(**kwargs)
        posts_of_category = self.get_queryset().posts_by_category
        context['object_list'] = posts_of_category
        context['title'] = f'Публикации в категории {title}'
        return context


class AllPostsListView(generic.ListView):
    template_name = 'posts.html'

    def get_queryset(self):
        queryset = Post.objects.all().prefetch_related(
            Prefetch('author')
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super(AllPostsListView, self).get_context_data(**kwargs)
        context['object_list'] = self.get_queryset()
        context['title'] = 'Публикации пользователей'
        return context


class MyPostsListView(LoginRequiredMixin, generic.ListView):
    template_name = 'posts.html'
    login_url = reverse_lazy('users:login')

    def get_queryset(self):
        queryset = Post.objects.prefetch_related(
            Prefetch('author')
        ).filter(author=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(MyPostsListView, self).get_context_data(**kwargs)
        context['title'] = 'Мои публикации'
        return context


class PostsByPk(generic.ListView):
    template_name = 'posts.html'

    def get_queryset(self, **kwargs):
        author_pk = self.kwargs.get('pk')
        queryset = Post.objects.filter(author_id__exact=author_pk)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostsByPk, self).get_context_data(**kwargs)
        context['object_list'] = self.get_queryset()
        return context


class PostDetailView(generic.DetailView):
    template_name = 'post_detail.html'

    def get_queryset(self):
        queryset = Post.objects.prefetch_related(
            Prefetch('author')
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data()
        context['obj'] = self.get_object(self.get_queryset())
        return context


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = PostForm
    model = Post
    template_name = 'form.html'
    success_url = reverse_lazy('posts:my-posts')

    def get_context_data(self, **kwargs):
        context = super(PostCreateView, self).get_context_data()
        context['form'] = self.form_class()
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCreateView, self).form_valid(form)


class PostUpdateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    fields = ['title', 'summary', 'content']
    success_url = reverse_lazy('posts:my-posts')
    template_name = 'form.html'


class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('posts:my-posts')
