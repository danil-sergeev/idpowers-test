from django.urls import path

from posts import views


app_name = 'posts'
urlpatterns = [
    path('all/', views.AllPostsListView.as_view(), name='posts'),
    path('my/', views.MyPostsListView.as_view(), name='my-posts'),
    path('detail/<int:pk>/<str:author.username>/', views.PostDetailView.as_view(), name='detail-post'),
    path('add/', views.PostCreateView.as_view(), name='add-post')
]
