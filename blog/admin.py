from django.contrib import admin
from .models import AboutPage, Category, Post, Comment

# Register your models here.

admin.site.register(AboutPage)



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}



class CommentInline(admin.TabularInline):
    model = Comment  
    extra = 0 
    fields = ('body', 'active')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('user',)



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish_date', 'status', 'category', "status", 'display_comment_count')
    list_filter = ('status', 'created_at', 'publish_date', 'author', 'category')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',) 
    date_hierarchy = 'publish_date'
    ordering = ('status', '-publish_date')

    inlines = [CommentInline]

    def display_comment_count(self, obj):
        return obj.comments.count()
    display_comment_count.short_description = 'Comments'



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('get_commentator_name', 'post', 'created_at', 'active')
    list_filter = ('active', 'created_at')
    search_fields = ('name', 'email', 'body')
    raw_id_fields = ('post',)

    actions = ['make_active', 'make_inactive']

    @admin.action(description='Mark selected comments as active')
    def make_active(self, request, queryset):
        queryset.update(active=True)
        self.message_user(request, f"{queryset.count()} comments marked as active.")

    @admin.action(description='Mark selected comments as inactive')
    def make_inactive(self, request, queryset):
        queryset.update(active=False)
        self.message_user(request, f"{queryset.count()} comments marked as inactive.")

    def save_model(self, request, obj, form, change):
        if not obj.user and request.user.is_authenticated:
            obj.user = request.user
        super().save_model(request, obj, form, change)


