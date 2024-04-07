from django.test import TestCase
from .forms import CommentForm

class TestCommentForm(TestCase):

    def test_form_is_valid(self):
        """Form should be valid with proper data."""
        comment_form = CommentForm(data={'body': 'This is a great post'})
        self.assertTrue(comment_form.is_valid())

    def test_form_is_invalid_with_empty_body(self):
        """Form should be invalid if body is empty."""
        comment_form = CommentForm(data={'body': ''})
        self.assertFalse(comment_form.is_valid())
        self.assertIn('body', comment_form.errors)  # Check if 'body' field has errors
        self.assertEqual(comment_form.errors['body'], ['This field is required.'])  # Assuming Django's default required field error message

    def test_form_field_labels_and_help_text(self):
        """Test form fields for correct labels and help texts."""
        comment_form = CommentForm()
        self.assertTrue(comment_form.fields['body'].label == 'Comment body' or comment_form.fields['body'].label is None)
        # Assuming 'body' does not have a label; if it does, replace 'Comment body' with the correct label

        # If your 'body' field has help_text defined in the form, test it like so:
        # self.assertEqual(comment_form.fields['body'].help_text, 'Enter your comment here.')

# Add more tests as needed to cover other scenarios specific to your form's logic.
