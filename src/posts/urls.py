from django.urls import path
from django.views.decorators.http import require_POST

from posts import views


app_name = 'posts'
urlpatterns = [
    path('all/', views.AllPostsListView.as_view(), name='posts'),
    path('my/', views.MyPostsListView.as_view(), name='my-posts'),
    path('detail/<int:pk>/', views.PostDetailView.as_view(), name='detail-post'),
    path('add/', views.PostCreateView.as_view(), name='add-post'),
    path('edit/<int:pk>/', views.PostUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', views.PostDeleteView.as_view(), name='delete'),
    path('<int:pk>/', views.PostsByPk.as_view(), name='posts-by-pk'),
    path('mark/<str:post_pk>/', require_POST(views.LeftMarkView.as_view()), name='mark'),
    path('category/<str:title>/', views.PostsByCategory.as_view(), name='posts-by-category')
]
