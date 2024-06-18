# users/tests.py
from django.test import TestCase
from .models import CustomUser


class CustomUserTestCase(TestCase):
    def setUp(self):
        CustomUser.objects.create(username="testuser", email="testuser@example.com", password="password123")

    def test_user_creation(self):
        user = CustomUser.objects.get(username="testuser")
        self.assertEqual(user.email, "testuser@example.com")