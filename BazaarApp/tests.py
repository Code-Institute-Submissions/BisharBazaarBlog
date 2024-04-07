from django.test import TestCase
from django.contrib.auth.models import User
from .models import BlogPost

class BlogPostModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        test_user = User.objects.create_user(username='testuser', password='12345')
        BlogPost.objects.create(title='Test Title', content='This is a test content', author=test_user)

    def test_blog_post_content(self):
        post = BlogPost.objects.get(id=1)
        expected_object_name = f'{post.title}'
        self.assertEqual(expected_object_name, 'Test Title')

    def test_blog_post_snippet(self):
        post = BlogPost.objects.get(id=1)
        expected_snippet = 'This is a test content...'
        self.assertEqual(post.snippet(), expected_snippet)

