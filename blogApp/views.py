import datetime

import xlwt
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.pagination import LimitOffsetPagination

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
from .serializers import PostSerializer


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




@api_view(['GET',])
def view_posts(request):
    search_word = request.query_params.get('search')
    download_file = request.query_params.get('download')
    filters = {'date_posted__gte': datetime.datetime.today() - datetime.timedelta(days=60)}

    posts = Post.objects.filter(Q(title__icontains=search_word) | Q(content__icontains=search_word) | Q(author__first_name__icontains=search_word), **filters)
    # paginate = LimitOffsetPagination()
    # paginated_posts = paginate.paginate_queryset(posts, request)

    serialized_posts = PostSerializer(posts, many=True)


    excel_data = []

    for data in serialized_posts.data:
        s = dict(data)
        excel_data.append(s)
    # return HttpResponse(serialized_posts.data)
    column_names = ['Image', 'Author', 'Title', 'Date Posted', 'Thumbnail', ]
    if download_file:
        return export_users_xls(column_names, excel_data)

    return JsonResponse(serialized_posts.data, safe=False)


def export_users_xls(column_names, excel_data):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="test-excel.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = column_names

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    for row_keys in excel_data:
        row_num += 1
        col_num = 0
        for key in row_keys:

            ws.write(row_num, col_num, row_keys[key], font_style)
            col_num += 1
    wb.save(response)
    return response