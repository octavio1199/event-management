from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from django.utils import timezone

from events.models import Event, Registration
from users.models import CustomUser


class EventViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(first_name='test', last_name='user',
                                                   email="testuser@example.com", password="password123")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.event = Event.objects.create(
            title="Teste de Evento",
            description="Descrição do evento de teste.",
            date=timezone.now() + timezone.timedelta(weeks=1),
            time=timezone.now().time(),
            location="Local do evento",
            organizer=self.user
        )
        self.registration = Registration.objects.create(event=self.event, participant=self.user)
        self.event_url = reverse('event-detail', kwargs={'pk': self.event.pk})

    def test_event_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('event-list'))
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_event_detail(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.event_url)
        self.assertEqual(response.data['title'], "Teste de Evento")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_event_create(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': "Teste de Evento",
            'description': "Descrição do evento de teste.",
            'date': '2024-06-30',
            'time': '12:30:00',
            'location': "Local do evento",
            'organizer': self.user.id
        }
        print("Eventos antes da criação: ", Event.objects.count())
        response = self.client.post(reverse('event-list'), data, format='json')
        print("Resposta do POST: ", response.data)
        print("Eventos após a criação: ", Event.objects.count())
        self.assertEqual(Event.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_event_update(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': "Evento Atualizado",
            'description': "Descrição do evento de teste.",
            'date': '2024-06-30',
            'time': '12:30:00',
            'location': "Local do evento",
            'organizer': self.user.id
        }
        response = self.client.put(self.event_url, data, format='json')
        self.event.refresh_from_db()
        self.assertEqual(self.event.title, "Evento Atualizado")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_event_delete(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.event_url)
        self.event.refresh_from_db()
        self.assertEqual(self.event.is_active, False)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # region Event Registration Tests
    def test_event_register(self):
        self.client.force_authenticate(user=self.user)
        register_url = reverse('event-register', kwargs={'pk': self.event.pk})
        response = self.client.post(register_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_event_confirm_registration(self):
        self.client.force_authenticate(user=self.user)
        register_url = reverse('event-register', kwargs={'pk': self.event.pk})
        self.client.post(register_url)
        confirm_registration_url = reverse('event-confirm-registration', kwargs={'pk': self.event.pk})
        response = self.client.post(confirm_registration_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_event_cancel_registration(self):
        self.client.force_authenticate(user=self.user)
        register_url = reverse('event-register', kwargs={'pk': self.event.pk})
        self.client.post(register_url)
        confirm_registration_url = reverse('event-confirm-registration', kwargs={'pk': self.event.pk})
        self.client.post(confirm_registration_url)
        cancel_registration_url = reverse('event-cancel-registration', kwargs={'pk': self.event.pk})
        response = self.client.put(cancel_registration_url)
        self.registration.refresh_from_db()  # Refresh the object from the database
        self.assertEqual(self.registration.is_active, False)
        self.assertEqual(self.registration.confirmed, False)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
