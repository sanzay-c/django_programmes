from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),  # List all posts
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),  # View a single post
    path('post/new/', PostCreateView.as_view(), name='post_create'),  # Create a new post
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),  # Edit a post
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),  # Delete a post
]
