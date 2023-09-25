"""
Tests for the Django admin modifications.
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from django.test import Client


class AdminSiteTests(TestCase):
    """Tests for Django admin."""
    def setUp(self):
        """Create user and client."""
        self.client = Client()
    def test_users_lists(self):
        self.assertContains(response, self.user.email)
    def test_edit_user_page(self):
        self.assertEqual(response.status_code, 200)
    def test_create_user_page(self):
        self.assertEqual(response.status_code, 200)