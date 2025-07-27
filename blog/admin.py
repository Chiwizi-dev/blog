from django.contrib import admin
from .models import AboutPage, Category, Post

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish_date', 'status', 'category', "status")
    list_filter = ('status', 'created_at', 'publish_date', 'author', 'category')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',) 
    date_hierarchy = 'publish_date'
    ordering = ('status', '-publish_date')

admin.site.register(AboutPage)