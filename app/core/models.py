"""
Database models.
"""
import uuid
import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator


def graphic_image_file_path(instance, filename):
    """Generate file path for new graphic image."""
    extension = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4()}{extension}"

    return os.path.join("uploads", "graphic", filename)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, tier=None, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError("User must have an email address.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.tier = tier
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, None, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


def get_default_thumbnail_heights_json():
    return {"heights": []}

class Tier(models.Model):
    """Tiers in the system."""

    name = models.CharField(max_length=255, unique=True)
    thumbnail_sizes = models.JSONField(default=get_default_thumbnail_heights_json)
    returns_original_image_link = models.BooleanField(default=False)
    returns_original_image_expiring_link = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    

class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""

    tier = models.ForeignKey(
        Tier, 
        on_delete=models.SET_NULL,
        null = True
    )
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"


class Graphic(models.Model):
    """Graphic object."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    image = models.ImageField(null=True, upload_to=graphic_image_file_path)