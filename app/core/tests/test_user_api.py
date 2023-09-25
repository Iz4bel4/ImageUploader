"""
Tests for the user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")
ME_URL = reverse("user:me")
class PublicUserApiTests(TestCase):
    """Test the public features of the user API."""
class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication."""
