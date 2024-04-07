from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import CommentForm
from .models import Post, Comment

class TestBlogViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(username="myUsername", password="myPassword", email="test@test.com")
        self.post = Post.objects.create(title="Blog title", author=self.user, slug="blog-title", excerpt="Blog excerpt", content="Blog content", status=1)

    def test_render_post_detail_page_with_comment_form(self):
        response = self.client.get(reverse('BazaarApp:post_detail', args=['blog-title']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Blog title")
        self.assertContains(response, "Blog content")
        self.assertIsInstance(response.context['comment_form'], CommentForm)

    def test_successful_comment_submission_redirects(self):
        self.client.force_login(self.user)  # Force login for simplicity
        post_data = {'body': 'This is a test comment.'}
        response = self.client.post(reverse('BazaarApp:post_detail', args=['blog-title']), post_data, follow=True)
        self.assertRedirects(response, reverse('BazaarApp:post_detail', args=['blog-title']))  # Assuming redirect back to the post detail
        self.assertContains(response, 'Comment submitted and awaiting approval')

    def test_unauthenticated_comment_submission(self):
        post_data = {'body': 'This is a test comment by an unauthenticated user.'}
        response = self.client.post(reverse('BazaarApp:post_detail', args=['blog-title']), post_data)
        # Assuming redirection to login page, modify as per your configuration
        self.assertRedirects(response, '/accounts/login/?next=' + reverse('BazaarApp:post_detail', args=['blog-title']))

    def test_comment_appears_after_approval(self):
        comment = Comment.objects.create(post=self.post, author=self.user, body="A test comment", approved=False)
        response = self.client.get(reverse('BazaarApp:post_detail', args=['blog-title']))
        self.assertNotContains(response, "A test comment")
        # Simulate comment approval
        comment.approved = True
        comment.save()
        response = self.client.get(reverse('BazaarApp:post_detail', args=['blog-title']))
        self.assertContains(response, "A test comment")
