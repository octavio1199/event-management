from unittest import mock

from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from events.models import Event, Registration
from reports.tasks import generate_event_report_task
from users.models import CustomUser


class EventReportTestCase(APITestCase):
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
        self.participant = CustomUser.objects.create_user(first_name='participant', last_name='user', email="participant@example.com", password="password123")
        self.registration = Registration.objects.create(participant=self.participant, event=self.event)
        self.url = reverse('event_report', kwargs={'event_id': self.event.id})

    def test_event_report(self):
        self.client.login(email='testuser@gmail.com', password='testpassword')

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'O relatório está sendo gerado e será enviado para o seu email em breve.')

    def test_unauthenticated_user_cannot_access_event_report(self):
        self.client.logout()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_non_organizer_cannot_access_event_report(self):
        other_user = CustomUser.objects.create_user(first_name='other', last_name='user',
                                                    email="otheruser@example.com", password="password123")
        self.client.login(email='otheruser@example.com', password='password123')
        other_token = Token.objects.create(user=other_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + other_token.key)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @mock.patch.object(generate_event_report_task, 'delay')
    def test_event_report_includes_participants(self, mock_delay):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'],
                         'O relatório está sendo gerado e será enviado para o seu email em breve.')
        mock_delay.assert_called_once_with(self.event.id, self.user.email)