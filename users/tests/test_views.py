import os

from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

from EventManager import settings
from ..models import CustomUser
from ..serializers import CustomUserSerializer


class AuthViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(first_name='test', last_name='user',
                                                   email="testuser@example.com", password="password123")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_signup(self):
        response = self.client.post(reverse('auth-signup'), data={'first_name':'new','last_name':'user', 'email': 'newuser@example.com', 'password': 'newpassword'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        response = self.client.post(reverse('auth-login'), data={'email': 'testuser@example.com', 'password': 'password123'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        response = self.client.post(reverse('auth-logout'))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ProfileViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(first_name='test', last_name='user',
                                                   email="testuser@example.com", password="password123")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_update_info(self):
        response = self.client.put(reverse('profile-update_info'), data={'first_name': 'New', 'last_name': 'User'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_upload_photo(self):
        image_path = os.path.join(settings.MEDIA_ROOT, 'profile_images', 'image.jpeg')
        with open(image_path, 'rb') as photo:
            response = self.client.post(reverse('profile-upload_photo'), data={'photo': photo})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_deactivate(self):
        response = self.client.post(reverse('profile-deactivate'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
