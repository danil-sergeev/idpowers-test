from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import Prefetch
from django.urls import reverse_lazy
from django.views import generic, View
from django.views.generic.edit import FormMixin
from django.http import HttpResponseForbidden

from posts.models import Post, Category, Comment, Mark
from posts.forms import PostForm, CommentForm, MarkForm


# Create your views here.

class AllPostsListView(generic.ListView):
    template_name = 'posts.html'

    def get_queryset(self):
        queryset = Post.objects.all().prefetch_related(
            Prefetch('author')
        )

        keywords = self.request.GET.get('q')
        sort = self.request.GET.get('sort')

        if keywords:
            print(keywords)
            query = SearchQuery(keywords)
            title_vector = SearchVector('title', weight='A')
            content_vector = SearchVector('content', weight='B')
            vectors = title_vector + content_vector
            queryset = queryset.annotate(search=vectors).filter(search=query)
            queryset = queryset.annotate(rank=SearchRank(vectors, query)).order_by('-rank')

        if sort:
            print(sort)
            queryset = queryset.order_by(sort)

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


class PostsByCategory(generic.ListView):
    template_name = 'posts.html'

    def get_queryset(self):
        title = self.kwargs['title']
        queryset = Post.objects.prefetch_related(
            Prefetch('category')
        ).filter(category__title__exact=title)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        title = self.kwargs['title']
        context = super(PostsByCategory, self).get_context_data(**kwargs)
        context['object_list'] = self.get_queryset()
        context['title'] = f'Публикации в категории {title}'
        return context


class PostDetailView(FormMixin, generic.DetailView):
    template_name = 'post_detail.html'
    form_class = CommentForm
    second_form_class = MarkForm

    def get_queryset(self):
        queryset = Post.objects.prefetch_related(
            Prefetch('comments')
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data()
        context['obj'] = self.get_object(self.get_queryset())
        if self.request.user.is_authenticated:
            context['form'] = self.get_form()
            context['mark_form'] = self.mark_form
        return context

    def post(self, request, *args, **kwargs):
        posting = self.get_object()

        if request.user == posting.author:
            return HttpResponseForbidden()

        if 'form1' in request.POST:
            form = self.get_form()
        else:
            form = self.get_form(self.second_form_class)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        posting = self.get_object()
        sender = self.request.user
        if form == self.form_class:
            content = form.cleaned_data.get("content")
            Comment.objects.create(post=posting, sender=sender, content=content)
        else:
            selected_mark = form.cleaned_data.get("select")
            Mark.objects.create(post=posting, sender=sender, mark=selected_mark)
        return super(PostDetailView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy("posts:detail-post", args={self.get_object().pk})


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


class LeftMarkView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        post_pk = self.kwargs.get('post_pk')
        post_obj = Post.objects.get(pk=post_pk)
        form = MarkForm(request.POST)
        if form.is_valid():
            mark = Mark()
            mark.post = post_obj
            mark.sender = request.user
            mark.save()
        else:
            form = MarkForm()
        return reverse_lazy('posts:detail-post', args={post_pk})


class CategoryListView(generic.ListView):
    template_name = 'main.html'

    def get_queryset(self):
        queryset = Category.objects.all()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['object_list'] = self.get_queryset()
        return context
