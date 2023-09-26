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

class PrivateGraphicApiTests(TestCase):
    """Test authenticated API requests."""
