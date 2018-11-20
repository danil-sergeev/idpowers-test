from django.urls import path

from tickets.views import ChatView, MyTicketsListView, CreateChatWithAdmin

app_name = 'tickets'
urlpatterns = [
    path('', MyTicketsListView.as_view(), name='my-tickets'),
    path('write-a-ticket/', CreateChatWithAdmin.as_view(), name='create-ticket'),
    path('<int:pk>/', ChatView.as_view(), name='ticket')
]