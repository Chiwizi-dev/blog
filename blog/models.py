from django.db import models
from django.conf import settings

from django.utils import timezone
from django.urls import reverse 
from django.utils.text import slugify 


# Create your models here.
User = settings.AUTH_USER_MODEL


class AboutPage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    profile_picture = models.ImageField(upload_to='about_page', default="about_page/about.png", blank=True, null=True)
    social_media_links = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, help_text="A URL-friendly short label.")
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug: 
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)




class PostManager(models.Manager):
    def published(self):
        return self.filter(status="published")


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish_date', help_text="A URL-friendly short label derived from the title, unique per publish date.")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    content = models.TextField()
    summary = models.TextField(max_length=1000, blank=True, help_text="A short summary of the post (max 500 characters).")
    thumbnail = models.ImageField(
        upload_to='blog/thumbnails/%Y/%m/%d/', blank=True,null=True, help_text="Thumbnail image for the blog post listing.")
    publish_date = models.DateTimeField(default=timezone.now) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='published'
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='posts'
    )
    # If you want tagging, consider using django-taggit:
    # from taggit.managers import TaggableManager
    # tags = TaggableManager(blank=True) # pip install django-taggit, add 'taggit' to INSTALLED_APPS

    objects = PostManager()

    class Meta:
        ordering = ['-publish_date']
        indexes = [
            models.Index(fields=['publish_date', 'slug']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish_date.year, self.publish_date.strftime('%m'), self.publish_date.strftime('%d'), self.slug])

    def save(self, *args, **kwargs):
        if not self.slug or (self.pk and not Post.objects.filter(pk=self.pk, title=self.title).exists()):
             self.slug = slugify(self.title)
        super().save(*args, **kwargs)