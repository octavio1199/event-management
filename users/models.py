from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Used for updating default create user behaviour
    """
    def create_user(self, email, password, **kwargs):
        # implement create user logic
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_no, password, **kwargs):
        # creates superuser.
        self.create_user(phone_no, password)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def perform_destroy(self):
        self.is_active = False
        self.save()