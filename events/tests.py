from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.utils import timezone

from events.models import Event
from users.models import User


class EventViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", email="testuser@example.com", password="password123")
        self.event = Event.objects.create(
            title="Teste de Evento",
            description="Descrição do evento de teste.",
            date=timezone.now() + timezone.timedelta(weeks=1),
            time=timezone.now().time(),
            location="Local do evento",
            organizer=self.user
        )
        self.event_url = reverse('event-detail', kwargs={'pk': self.event.pk})

    def test_event_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('event-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_event_detail(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.event_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_event_create(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': "Teste de Evento",
            'description': "Descrição do evento de teste.",
            'date': '2024-06-21',
            'time': '12:30:00',
            'location': "Local do evento",
            'organizer': self.user.id
        }
        response = self.client.post(reverse('event-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_event_update(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': "Evento Atualizado",
            'description': "Descrição do evento de teste.",
            'date': '2024-06-21',
            'time': '12:30:00',
            'location': "Local do evento",
            'organizer': self.user.id
        }
        response = self.client.put(self.event_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_event_delete(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.event_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

