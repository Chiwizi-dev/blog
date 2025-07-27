from django.shortcuts import render, get_object_or_404
from .models import AboutPage, Category, Post

from django.http import HttpResponse


# Create your views here.


def home(request):
    posts = Post.objects.published()
    posts_count = posts.count()

    context = {"posts": posts, "posts_count": posts_count}
    return render(request, "blog/home.html", context)


def about_page(request):
    about = get_object_or_404(AboutPage, id=1)
    context = {"about": about}

    return render(request, "blog/about_page.html", context)


def post_detail(request, yr, mt, dt, slug):
    object = get_object_or_404(
        Post,
        publish_date__year=yr,
        publish_date__month=mt,
        publish_date__day=dt,
        slug= slug
    )

    context = {"post": object}

    return render(request, "blog/post_detail.html", context)