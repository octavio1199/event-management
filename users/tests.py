# users/tests.py
from rest_framework.test import APITestCase, APIClient

from .models import User
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from .serializers import UserSerializer


class CustomUserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", first_name='test', last_name='user',
                                        email="testuser@example.com", password="password123")

    def test_user_creation(self):
        user = User.objects.get(username="testuser")
        self.assertEqual(user.email, "testuser@example.com")

    def test_perform_destroy(self):
        self.user.perform_destroy(self.user)
        self.assertFalse(self.user.is_active)


class UserViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username="testuser", email="testuser@example.com", password="password123")
        self.admin = User.objects.create_superuser(username="admin", email="admin@example.com", password="admin123")
        self.user_url = reverse('user-detail', kwargs={'pk': self.user.pk})

    def test_user_list(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(reverse('user-list'))
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_retrieve(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.user_url)
        serializer = UserSerializer(self.user)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_create(self):
        data = {'username': 'newuser', 'first_name': 'new', 'last_name': 'user', 'email': 'newuser@example.com',
                'password': 'password123'}
        response = self.client.post(reverse('user-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_update(self):
        self.client.force_authenticate(user=self.user)
        data = {'username': 'updateduser', 'first_name': 'updated', 'last_name': 'user',
                'email': 'updateduser@example.com', 'password': 'password123'}
        response = self.client.put(self.user_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')

    def test_user_partial_update(self):
        self.client.force_authenticate(user=self.user)
        data = {'username': 'partialupdateduser'}
        response = self.client.patch(self.user_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'partialupdateduser')

    def test_user_destroy(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.user_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=self.user.pk, is_active=True).exists())

    def test_admin_list_users(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_admin_list_users(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_update_other_user(self):
        self.client.force_authenticate(user=self.admin)
        data = {'username': 'updateduser', 'email': 'updateduser@example.com', 'password': 'password123'}
        other_user_url = reverse('user-detail', kwargs={'pk': self.user.pk})
        response = self.client.put(other_user_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_admin_update_other_user(self):
        other_user = User.objects.create(username="otheruser", email="otheruser@example.com", password="password123")
        other_user_url = reverse('user-detail', kwargs={'pk': other_user.pk})
        self.client.force_authenticate(user=self.user)
        data = {'username': 'updateduser', 'email': 'updateduser@example.com', 'password': 'password123'}
        response = self.client.put(other_user_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
