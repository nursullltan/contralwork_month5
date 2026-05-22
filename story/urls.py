from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.PostListAPIView.as_view()),
    path('posts/<int:id>/', views.PostDetailAPIView.as_view()),
    path('posts/<int:post_id>/comments/', views.CommentListAPIView.as_view()),
    path('comments/<int:id>/', views.CommentDetailAPIView.as_view()),
]