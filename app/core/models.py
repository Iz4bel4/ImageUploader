from django.db import models
class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, tier=None, password=None, **extra_fields):
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        return user
class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
