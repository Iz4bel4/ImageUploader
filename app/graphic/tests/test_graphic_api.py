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

from core.models import Graphic, Tier

from graphic.serializers import GraphicSerializer

from graphic.serializers import (
    GraphicSerializer,
)


GRAPHICS_URL = reverse("graphic:graphic-list")


def detail_url(graphic_id):
    """Create and return a graphic detail URL."""
    return reverse("graphic:graphic-detail", args=[graphic_id])


def expirational_url(graphic_id, target_duration_seconds):
    """Create and return a graphic detail URL."""
    return reverse(
        "graphic:graphic-get-image-expirational-link",
        args=[graphic_id, target_duration_seconds],
    )


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


def create_thumbnail_image_tier():
    """Create and return a new tier."""
    return Tier.objects.create(
        name="Test_thumbnail", thumbnail_sizes={"heights": ["200"]}
    )


def create_expirational_image_tier():
    """Create and return a new tier."""
    return Tier.objects.create(
        name="Test_expirational",
        returns_original_image_expiring_link=True,
    )


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
        other_user = create_user(
            email="other@example.com", tier=self.tier, password="test123"
        )

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

    def test_get_single_graphic(self):
        """Test get graphic."""
        graphic = create_graphic(user=self.user)

        url = detail_url(graphic.id)
        response = self.client.get(url)

        serializer = GraphicSerializer(graphic)
        self.assertEqual(response.data, serializer.data)

    def test_create_graphic(self):
        """Test creating a graphic."""
        with tempfile.NamedTemporaryFile(suffix=".jpg") as image_file:
            img = Image.new("RGB", (10, 10))
            img.save(image_file, format="JPEG")
            image_file.seek(0)
            payload = {"image": image_file}
            response = self.client.post(GRAPHICS_URL, payload, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        graphic = Graphic.objects.get(id=response.data["id"])
        self.assertEqual(graphic.user, self.user)
        self.assertIn("image", response.data)
        self.assertTrue(os.path.exists(graphic.image.path))

    def test_getting_original_image_link(self):
        """Test getting original image."""
        graphic = create_graphic(user=self.user)

        url = detail_url(graphic.id)
        response = self.client.get(url)
        self.assertTrue("image" in response.data)

    def test_not_getting_original_image_link(self):
        """Test not getting original image, as you don't have a tier to get one."""
        other_user = create_user(
            email="other@example.com", tier=self.tier_nothing, password="test123"
        )
        graphic = create_graphic(user=other_user)

        url = detail_url(graphic.id)
        response = self.client.get(url)
        self.assertFalse("image" in response.data)

    def test_getting_thumbnail_image_link(self):
        """Test getting thumbnail image."""
        other_user = create_user(
            email="other@example.com", tier=self.tier_thumbnail, password="test123"
        )
        graphic = create_graphic(user=other_user)

        url = detail_url(graphic.id)
        response = self.client.get(url)
        self.assertTrue("thumbnail_200" in response.data)

    def test_not_getting_thumbnail_image_link(self):
        """Test not getting original image, as you don't have a tier to get one."""
        other_user = create_user(
            email="other@example.com", tier=self.tier_nothing, password="test123"
        )
        graphic = create_graphic(user=other_user)

        url = detail_url(graphic.id)
        response = self.client.get(url)
        self.assertFalse("image_200" in response.data)

    def test_getting_expirational_image_link(self):
        """Test getting expirational image link."""
        other_user = create_user(
            email="other@example.com", tier=self.tier_expirational, password="test123"
        )
        graphic = create_graphic(user=other_user)

        url = expirational_url(graphic.id, 600)
        response = self.client.get(url)
        self.assertTrue("image" in response.data)

    def test_not_getting_expirational_image_link_because_of_tier(self):
        """Test not getting expirational image link, as you don't have a tier to get one."""
        other_user = create_user(
            email="other@example.com", tier=self.tier_nothing, password="test123"
        )
        graphic = create_graphic(user=other_user)

        url = expirational_url(graphic.id, 600)
        response = self.client.get(url)
        self.assertFalse("image" in response.data)

    def test_not_getting_expirational_image_link_because_of_wrong_value_range(self):
        """Test not getting expirational image link, as you don't have a tier to get one."""
        other_user = create_user(
            email="other@example.com", tier=self.tier_expirational, password="test123"
        )
        graphic = create_graphic(user=other_user)

        url = expirational_url(graphic.id, 5)
        response = self.client.get(url)
        self.assertFalse("image" in response.data)
