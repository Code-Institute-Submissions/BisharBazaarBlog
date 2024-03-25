from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    """
    Lists fields for display in admin, fileds for search,
    field filters, fields to prepopulate and rich-text editor.
    """

    list_display = ('title', 'slug', 'status', 'created_on')
    search_fields = ['title', 'content']
    list_filter = ('status', 'created_on',)
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Registers Comment model for admin site.
    """

    list_display = ('body', 'post', 'author', 'created_on', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ('body', 'author__username', 'post__title')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        """
        Marks selected comments as approved.
        """
        queryset.update(approved=True)


# Register your models here.
