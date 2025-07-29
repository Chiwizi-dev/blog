from django.urls import path
from .views import home, about_page, post_detail, user_posts


app_name="blog"

urlpatterns = [
    path("<int:yr>/<int:mt>/<int:dt>/<slug:slug>/",post_detail, name="post_detail"),
    path("category/<slug:category>/", home, name="categories"),
    path("blog/about_page/", about_page, name="about_page"),
    path("user_posts/", user_posts, name="user_posts"),
    path("", home, name="home"),
]