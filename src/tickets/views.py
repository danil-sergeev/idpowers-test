from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic.edit import FormMixin
from django.views.generic import DetailView, ListView, CreateView
from django.db.models import Prefetch, Q

from tickets.models import Chat, ChatMessage
from tickets.forms import ChatForm, ChatCreateForm


# Create your views here.

profile = get_user_model()


class MyTicketsListView(LoginRequiredMixin, ListView):
    template_name = 'chat/chat_list.html'

    def get_queryset(self):
        return Chat.objects.filter(
            Q(customer=self.request.user) | Q(admin=self.request.user)
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MyTicketsListView, self).get_context_data(**kwargs)
        context['object_list'] = self.get_queryset()
        return context


class CreateChatWithAdmin(LoginRequiredMixin, CreateView):
    form_class = ChatCreateForm
    model = Chat
    template_name = 'form.html'
    success_url = reverse_lazy('tickets:my-tickets')

    def get_context_data(self, **kwargs):
        context = super(CreateChatWithAdmin, self).get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context

    # чет закостылил тут. не сейвилась форма как - то
    def form_valid(self, form):
        admin_pk = self.request.POST.get("admin")
        admin = profile.objects.get(pk=admin_pk)
        form.instance.customer = self.request.user
        form.instance.admin = admin
        return super(CreateChatWithAdmin, self).form_valid(form)


class ChatView(UserPassesTestMixin, LoginRequiredMixin, FormMixin, DetailView):
    template_name = 'chat/chat.html'
    model = Chat
    form_class = ChatForm
    success_url = './'

    def test_func(self):
        user = self.request.user
        chat_obj = self.get_object()
        return user == chat_obj.admin or user == chat_obj.customer

    def get_queryset(self):
        queryset = Chat.objects.filter(
            Q(admin=self.request.user) | Q(customer=self.request.user)
        ).prefetch_related(
            Prefetch('messages')
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        chat = self.get_object()
        user = self.request.user
        message = form.cleaned_data.get("message")
        ChatMessage.objects.create(sender=user, chat=chat, message=message)
        return super(ChatView, self).form_valid(form)
