from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from cloudinary.models import CloudinaryField

STATUS_CHOICES = ((0, "Draft"), (1, "Published"))
ORDER_STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Processing', 'Processing'),
    ('Shipped', 'Shipped'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled'),
)

class Product(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255, default='Default Brand')
    description = models.TextField()
    specifications = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = CloudinaryField('image', default='placeholder')  # Ensure you have a placeholder or set it to blank=True if optional

    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bazaarapp_posts")
    featured_image = CloudinaryField('image', default='placeholder')
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    excerpt = models.TextField(blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_on']
    
    def __str__(self):
        return f"{self.title} | written by {self.author.username}"

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bazaarapp_comments")
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_on']
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='Pending')
    
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # This could reflect the price at the time of order if prices can change
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
