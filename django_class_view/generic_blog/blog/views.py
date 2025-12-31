from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post

# List all posts
class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"

# View a single post
class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

# Create a new post
class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = "blog/post_form.html"
    success_url = reverse_lazy('post_list')

# Update an existing post
class PostUpdateView(UpdateView):
    model = Post
    fields = '__all__'
    template_name = "blog/post_form.html"
    success_url = reverse_lazy('post_list')

# Delete a post
class PostDeleteView(DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy('post_list')
