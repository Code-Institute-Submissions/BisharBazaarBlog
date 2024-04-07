from django import forms
from .models import Comment, Product, Post  # Corrected import statement

class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your comment here'}))

    class Meta:
        model = Comment
        fields = ('body',)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'brand', 'description', 'specifications', 'price', 'image']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'featured_image']
