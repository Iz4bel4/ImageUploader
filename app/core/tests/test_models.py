"""
Tests for models.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from unittest.mock import patch
from decimal import Decimal
from core import models


def create_user(email="user@example.com", tier=None, password="testpass123"):
    """Create a return a new user."""
    return get_user_model().objects.create_user(email, tier, password)


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = "test@example.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            tier=None,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.com", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, None, "sample123")
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", None, "test123")

    def user(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            "test@example.com",
            "test123",
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_graphic(self):
        """Test creating a graphic is successful."""
        user = get_user_model().objects.create_user(
            "test@example.com",
            None,
            "testpass123",
        )
        graphic = models.Graphic.objects.create(
            user=user,
        )
        self.assertEqual(graphic.user, user)

    @patch("core.models.uuid.uuid4")
    def test_graphic_file_name_uuid(self, mock_uuid):
        """Test generating image path."""
        uuid = "test-uuid"
        mock_uuid.return_value = uuid
        file_path = models.graphic_image_file_path(None, "example.jpg")

        self.assertEqual(file_path, f"uploads/graphic/{uuid}.jpg")
