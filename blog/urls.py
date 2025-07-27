from django.urls import path
from .views import home, about_page, post_detail


app_name="blog"

urlpatterns = [
    path("<int:yr>/<int:mt>/<int:dt>/<slug:slug>/",post_detail, name="post_detail"),
    path("blog/about_page/", about_page, name="about_page"),
    path("", home, name="home"),
]