from django.urls import path
from .views import home, about_page, post_detail, user_posts, create, post_edit


app_name="blog"

urlpatterns = [
    path("detail/<int:yr>/<int:mt>/<int:dt>/<slug:slug>/",post_detail, name="post_detail"),
    path("detail/edit/<int:yr>/<int:mt>/<int:dt>/<slug:slug>/", post_edit, name="post_edit"),
    path("category/<slug:category>/", home, name="categories"),
    path("about_page/", about_page, name="about_page"),
    path("user_posts/", user_posts, name="user_posts"),
    path("create/", create, name="create"),
    path("", home, name="home"),
]