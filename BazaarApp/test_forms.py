from django.test import TestCase
from BazaarApp.forms import CommentForm  # Adjust the import path for the form

# Create your tests here.
class TestCommentForm(TestCase):

    def test_form_is_valid(self):
        comment_form = CommentForm(data={'body': 'This is a great post'})
        self.assertTrue(comment_form.is_valid(), msg="Form is invalid")

    def test_form_is_invalid(self):
        comment_form = CommentForm(data={'body': ''})
        self.assertFalse(comment_form.is_valid(), msg="Form is valid")
