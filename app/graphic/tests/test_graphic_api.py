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
class PublicGraphicAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        response = self.client.get(GRAPHICS_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


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

    def test_graphic_list_limited_to_user(self):
        """Test list of graphics is limited to authenticated user."""
        other_user = create_user(email="other@example.com", tier=self.tier, password="test123")

        create_graphic(user=other_user)
        create_graphic(user=self.user)
        
        response = self.client.get(GRAPHICS_URL)

        graphics = Graphic.objects.filter(user=self.user).order_by("-id")
        serializer = GraphicSerializer(graphics, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_multiple_graphics(self):
        """Test get a list of graphics."""
        create_graphic(user=self.user)
        create_graphic(user=self.user)

        response = self.client.get(GRAPHICS_URL)

        graphics = Graphic.objects.all().order_by("-id")
        serializer = GraphicSerializer(graphics, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
