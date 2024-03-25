from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import CommentForm
from .models import Post

class TestBazaarAppViews(TestCase):
    def setUp(self):
        """Create a superuser and a blog post"""
        self.user = User.objects.create_superuser(
            username="myUsername", password="myPassword", email="test@test.com")
        self.post = Post.objects.create(
            title="Blog title",
            author=self.user,
            slug="blog-title",
            excerpt="Blog excerpt",
            content="Blog content",
            status=1
        )

    def test_render_post_detail_page_with_comment_form(self):
        """Verifies a single blog post containing a comment form is returned"""
        response = self.client.get(reverse('post_detail', args=['blog-title']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, b"Blog title")
        self.assertContains(response, b"Blog content")
        self.assertIsInstance(response.context['comment_form'], CommentForm)

    def test_successful_comment_submission(self):
        """Test for posting a comment on a post"""
        self.client.login(username="myUsername", password="myPassword")
        post_data = {
            'body': 'This is a test comment.'
        }
        response = self.client.post(reverse('post_detail', args=['blog-title']), post_data)
        self.assertEqual(response.status_code, 302)  # Check for redirect after successful submission
        # You may want to verify that the comment is saved in the database as well
        self.assertTrue(Post.objects.filter(comments__body='This is a test comment').exists())

    def test_unsuccessful_comment_submission(self):
        """Test for posting a comment with invalid data"""
        self.client.login(username="myUsername", password="myPassword")
        post_data = {}  # Invalid data, comment body is missing
        response = self.client.post(reverse('post_detail', args=['blog-title']), post_data)
        self.assertEqual(response.status_code, 200)  # Form submission should return the same page
        # You may want to verify that the comment is not saved in the database
        self.assertFalse(Post.objects.filter(comments__body='This is a test comment').exists())
