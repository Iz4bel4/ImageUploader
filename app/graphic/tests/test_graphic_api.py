"""
Tests for graphic APIs.
"""
from decimal import Decimal
import tempfile
import os

from PIL import Image

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Graphic,
    Tier
)

from graphic.serializers import GraphicSerializer

from graphic.serializers import (
    GraphicSerializer,
)


GRAPHICS_URL = reverse("graphic:graphic-list")

def detail_url(graphic_id):
    """Create and return a graphic detail URL."""
    return reverse("graphic:graphic-detail", args=[graphic_id])
def create_graphic(user):
    """Create and return a sample graphic."""
    graphic = Graphic.objects.create(user=user)
    return graphic

def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)

def create_original_image_tier():
    """Create and return a new tier."""
    return Tier.objects.create(name="Test_original", returns_original_image_link=True)

def create_no_image_tier():
    """Create and return a new tier."""
    return Tier.objects.create(name="Test_nothing")
class PrivateGraphicApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.tier = create_original_image_tier()
        self.tier_nothing = create_no_image_tier()
        self.tier_thumbnail = create_thumbnail_image_tier()
        self.tier_expirational = create_expirational_image_tier()

        self.user = get_user_model().objects.create_user(
            "user@example.com",
            self.tier,
            "testpass123",
        )
        self.client.force_authenticate(self.user)
