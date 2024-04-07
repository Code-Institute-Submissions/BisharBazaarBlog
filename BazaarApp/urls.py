# BazaarApp/urls.py
from django.urls import path
from . import views

app_name = 'BazaarApp'  # Define the application namespace correctly

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('blog/<slug:slug>/', views.post_detail, name='post_detail'),
    path('blog/<slug:slug>/edit_comment/<int:comment_id>/', views.comment_edit, name='comment_edit'),
    path('blog/<slug:slug>/delete_comment/<int:comment_id>/', views.comment_delete, name='comment_delete'),
    path('products/', views.ProductList.as_view(), name='product_list'),
    path('products/<int:pk>/', views.ProductDetail.as_view(), name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('update-cart/<int:product_id>/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-history/', views.order_history, name='order_history'),
    # Remove the 'about' line from here
]

