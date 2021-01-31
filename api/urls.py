from django.urls import path
from api import views as api_views

urlpatterns = [
    path('list-blogs/', api_views.view_posts),
    ]
