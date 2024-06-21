from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.backends.utils import logger
from django.utils import timezone

from EventManager.settings import EMAIL_HOST_USER
from events.models import Registration, Event
from notifications.models import Notification
from users.models import CustomUser


@shared_task
def send_notification(user_id, event_id, message):
    receiver = CustomUser.objects.get(id=user_id)
    event = Event.objects.get(id=event_id)
    Notification.objects.create(event=event, receiver=receiver, message=message)
    send_mail(
        'Atualização de Evento',
        message,
        EMAIL_HOST_USER,
        [receiver.email],
        fail_silently=False,
    )


@shared_task
def notify_one_week_before_event():
    one_week_before = timezone.now() + timezone.timedelta(weeks=1)
    events = Event.objects.filter(date=one_week_before.date())
    for event in events:
        registrations = Registration.objects.filter(event=event)
        for registration in registrations:
            send_notification.delay(
                user_id=registration.user.id,
                event_id=event.id,
                message=f"Alerta: O evento '{event.title}' acontecerá em uma semana."
            )


@shared_task
def notify_one_day_before_event():
    one_day_before = timezone.now() + timezone.timedelta(days=1)
    events = Event.objects.filter(date=one_day_before.date())
    for event in events:
        registrations = Registration.objects.filter(event=event)
        for registration in registrations:
            send_notification.delay(
                user_id=registration.user.id,
                event_id=event.id,
                message=f"Alerta: O evento '{event.title}' acontecerá amanhã."
            )


@shared_task
def send_confirmation_email(user_id, event_id):
    user = CustomUser.objects.get(id=user_id)
    event = Event.objects.get(id=event_id)
    confirmation_url = f"http://localhost:8000/api/events/{event_id}/confirm_registration/"
    message = f'Clique no link para confirmar sua inscrição: {confirmation_url}'
    send_notification.delay(user_id=user.id, event_id=event.id, message=message)