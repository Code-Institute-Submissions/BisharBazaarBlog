from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Post, Comment
from .forms import CommentForm
from django.views.generic import ListView

class PostList(ListView):
    """
    Returns all published posts in :model:`BazaarApp.Post`
    and displays them in a page of six posts.
    **Context**

    ``queryset``
        All published instances of :model:`BazaarApp.Post`
    ``paginate_by``
        Number of posts per page.

    **Template:**

    :template:`BazaarApp/index.html`
    """
    model = Post
    template_name = "BazaarApp/index.html"
    paginate_by = 6

def post_detail(request, slug):
    """
    Display an individual :model:`BazaarApp.Post`.

    **Context**

    ``post``
        An instance of :model:`BazaarApp.Post`.
    ``comments``
        All approved comments related to the post.
    ``comment_count``
        A count of approved comments related to the post.
    ``comment_form``
        An instance of :form:`BazaarApp.CommentForm`

    **Template:**

    :template:`BazaarApp/post_detail.html`
    """
    post = get_object_or_404(Post, slug=slug, status=1)
    comments = post.comments.filter(approved=True).order_by("-created_on")
    comment_count = comments.count()

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, 'Comment submitted and awaiting approval')
            return HttpResponseRedirect(reverse('post_detail', kwargs={'slug': slug}))
    else:
        comment_form = CommentForm()

    return render(
        request,
        "BazaarApp/post_detail.html",
        {
            "post": post,
            "comments": comments,
            "comment_count": comment_count,
            "comment_form": comment_form
        },
    )

def comment_edit(request, slug, comment_id):
    """
    Display an individual comment for edit.

    **Context**

    ``post``
        An instance of :model:`BazaarApp.Post`.
    ``comment``
        A single comment related to the post.
    ``comment_form``
        An instance of :form:`BazaarApp.CommentForm`
    """
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST, instance=comment)
        if comment_form.is_valid() and comment.author == request.user:
            comment_form.save()
            messages.success(request, 'Comment Updated!')
        else:
            messages.error(request, 'Error updating comment!')
        return HttpResponseRedirect(reverse('post_detail', kwargs={'slug': slug}))

    return render(
        request,
        "BazaarApp/comment_edit.html",
        {
            "comment": comment,
            "comment_form": CommentForm(instance=comment)
        },
    )

def comment_delete(request, slug, comment_id):
    """
    Delete an individual comment.

    **Context**

    ``post``
        An instance of :model:`BazaarApp.Post`.
    ``comment``
        A single comment related to the post.
    """
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.method == "POST" and comment.author == request.user:
        comment.delete()
        messages.success(request, 'Comment deleted!')
    else:
        messages.error(request, 'You can only delete your own comments!')
    
    return HttpResponseRedirect(reverse('post_detail', kwargs={'slug': slug}))

