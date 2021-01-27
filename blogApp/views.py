from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin


# Create your views here.
# def home(request):
#     posts = Post.objects.all()
#     title = 'Home'
#     return render(request, 'blogApp/home.html', context={'posts': posts,
#                                                          'title': title})


class PostListView(ListView):
    model = Post
    template_name = 'blogApp/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 4


class PostDetailView(DetailView):
    model = Post


class PostCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Post
    success_message = "Your blog post \"%(title)s\" has been posted"
    fields = [
        'title',
        'content',
        'thumbnail',
    ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = [
        'title',
        'content',
        'thumbnail',
    ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/blog/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class UserPostListView(ListView):
    model = Post
    template_name = 'blogApp/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


def about(request):
    title = "About"
    return render(request, 'blogApp/about.html', context={'title': title})
