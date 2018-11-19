from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.urls import reverse_lazy
from django.views import generic


from posts.models import Post
from posts.forms import PostForm
# Create your views here.


class AllPostsListView(generic.ListView):
    template_name = 'posts.html'

    def get_queryset(self):
        queryset = Post.objects.select_related(
            Prefetch('author')
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super(AllPostsListView, self).get_context_data(**kwargs)
        return context


class MyPostsListView(LoginRequiredMixin, generic.ListView):
    template_name = 'posts.html'
    login_url = reverse_lazy('users:login')

    def get_queryset(self):
        queryset = Post.objects.select_related(
            Prefetch('author')
        ).filter(author=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(MyPostsListView, self).get_context_data(**kwargs)
        return context


class PostDetailView(generic.DetailView):
    template_name = 'post_detail.html'

    def get_queryset(self):
        queryset = Post.objects.select_related(
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
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super(PostCreateView, self).get_context_data()
        context['form'] = self.form_class()
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCreateView, self).form_valid(form)


