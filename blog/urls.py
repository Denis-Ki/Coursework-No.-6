from django.urls import path
from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from blog.views import BlogDetailView, BlogListView

app_name = BlogConfig.name

urlpatterns = [
    path("blog_list/", BlogListView.as_view(), name="blog_list"),
    path(
        "blog_detail/<int:pk>/",
        cache_page(60)(BlogDetailView.as_view()),
        name="blog_detail",
    ),
]
