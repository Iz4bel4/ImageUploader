"""
Tests for models.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from unittest.mock import patch
from decimal import Decimal
from core import models
class ModelTests(TestCase):
    """Test models."""
