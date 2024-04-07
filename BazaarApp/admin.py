from django.contrib import admin
from .models import Product, Post, Comment, Order, OrderItem

# Optional: Define custom admin classes to customize the admin interface

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'price')
    search_fields = ('name', 'brand')

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_on')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'body', 'post', 'created_on', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ('author', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'total_price', 'status')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'status')

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    search_fields = ('order__user__username', 'product__name')

# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
