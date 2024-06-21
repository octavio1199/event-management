from users.models import CustomUser
from django.test import TestCase


class UserTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(first_name='test', last_name='user',
                                              email="testuser@example.com", password="password123")

    def test_user_creation(self):
        user = CustomUser.objects.get(email="testuser@example.com")
        self.assertEqual(user.first_name, "test")

    def test_perform_destroy(self):
        self.user.perform_destroy()
        self.assertFalse(self.user.is_active)
