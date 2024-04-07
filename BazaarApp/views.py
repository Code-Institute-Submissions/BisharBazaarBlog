from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Post, Product, Comment, Order, OrderItem
from .forms import CommentForm

# Displaying a list of blog posts, filtered by status.
class PostList(ListView):
    model = Post
    template_name = "BazaarApp/index.html"
    paginate_by = 6
    queryset = Post.objects.filter(status=1)  # Ensure you only display published posts.

# Detail view for a single post, including comments and a form to submit new comments.
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status=1)
    comments = post.comments.filter(approved=True).order_by("-created_on")

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            messages.success(request, 'Comment submitted and awaiting approval')
            return redirect('post_detail', slug=post.slug)
    else:
        comment_form = CommentForm()

    context = {
        "post": post,
        "comments": comments,
        "comment_form": comment_form
    }
    return render(request, "BazaarApp/post_detail.html", context)

# Listing all products
class ProductList(ListView):
    model = Product
    template_name = "BazaarApp/product_list.html"

# Detail view for a specific product
class ProductDetail(DetailView):
    model = Product
    template_name = "BazaarApp/product_detail.html"

@login_required
def comment_edit(request, slug, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    post = get_object_or_404(Post, slug=slug)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your comment has been updated.')
            return redirect('post_detail', slug=slug)
    else:
        form = CommentForm(instance=comment)

    context = {'form': form, 'post': post}
    return render(request, 'BazaarApp/edit_comment.html', context)

@login_required
def comment_delete(request, slug, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user == comment.author:
        comment.delete()
        messages.success(request, "Comment successfully deleted.")
    else:
        messages.error(request, "You do not have permission to delete this comment.")
    
    return redirect('post_detail', slug=slug)

# Adding a product to the shopping cart
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    messages.success(request, f"{product.name} added to cart successfully!")
    return redirect('product_list')

# Displaying the contents of the shopping cart
@login_required
def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_products = []
    total_price = 0.00

    for id, quantity in cart.items():
        product = get_object_or_404(Product, id=id)
        total = product.price * quantity
        total_price += total
        cart_products.append({'product': product, 'quantity': quantity, 'total': total})

    context = {'cart_products': cart_products, 'total_price': total_price}
    return render(request, 'BazaarApp/cart_detail.html', context)

# Updating the quantity of a specific product in the cart
@login_required
def update_cart(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})

        if quantity > 0:
            cart[str(product_id)] = quantity
        else:
            cart.pop(str(product_id), None)

        request.session['cart'] = cart
        messages.success(request, "Cart updated successfully!")
    return redirect('cart_detail')

# Removing a product from the cart
@login_required
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart.pop(str(product_id))
        request.session['cart'] = cart
        messages.success(request, "Product removed from cart.")
    
    return redirect('cart_detail')

# Simplified checkout process; adjust according to your business logic
@login_required
def checkout(request):
    request.session.pop('cart', None)  # Clears the cart after checkout
    messages.success(request, "Checkout successful. Thank you for your order!")
    return redirect('home')

# Displaying the user's order history
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'BazaarApp/order_history.html', {'orders': orders})
