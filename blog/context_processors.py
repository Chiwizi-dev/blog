from blog.models import Post, Category




def posts_count(request):
    categories = Category.objects.all()
    posts_count = Post.objects.published().count()
    return {
        "posts_count": posts_count, "categories":categories
    }