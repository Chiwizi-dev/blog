from django.shortcuts import render, get_object_or_404, redirect
from .models import AboutPage, Category, Post
from .forms import CreateForm, EditForm

from django.contrib import messages
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required


# Create your views here.


def home(request, category=None):
    posts = None
    if category is not None:
        posts = Post.objects.filter(category__slug=category, status="published")
    else:
        posts = Post.objects.published()
    
    
    # posts_count = posts.count()

    # "posts_count": posts_count
    context = {"posts": posts, "user_posts": user_posts}
    return render(request, "blog/home.html", context)



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



def about_page(request):
    about = get_object_or_404(AboutPage, id=1)
    context = {"about": about}

    return render(request, "blog/about_page.html", context)



def user_posts(request):
    posts = Post.objects.filter(status="published", author_id=request.user.id)
    print(posts)

    context = {
        "posts": posts
    }

    return render(request, "blog/user_posts.html", context)



@login_required(login_url="/accounts/login/")
def create(request):
    if request.method == "POST":
        form = CreateForm(request.POST)

        if form.is_valid():
            post_instance = form.save(commit=False)
            post_instance.author = request.user
            post_instance.save()

            return redirect("blog:home")
        else:
            messages.error(request, "Please address the errors listed below")
    else:
        form = CreateForm()
    
    context = {"form": form}
    return render(request, "blog/create.html", context)



@login_required(login_url="/accounts/login/")
def post_edit(request, yr, mt, dt, slug):
    obj = get_object_or_404(
        Post,
        publish_date__year=yr,
        publish_date__month=mt,
        publish_date__day=dt,
        slug=slug
    )

    if obj.author != request.user:
        messages.error(request, "You don't have permission to edit this post!")
        return redirect("blog:post_detail")

    if request.method == "POST":
        form = EditForm(request.POST, request.FILES, instance=obj)

        if form.is_valid():
            form.save()
            return redirect(
                'blog:post_detail', 
                yr=obj.publish_date.year, 
                mt=obj.publish_date.month, 
                dt=obj.publish_date.day, 
                slug=obj.slug
            )
        else:
            messages.error(request, "Please address the errors highlighted below")
    else:
        form = EditForm(instance=obj)
    
    context = context = {"form": form, "post": obj}
    return render(request, "blog/post_edit.html", context)