from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils import timezone

from events.models import Registration, Event
from users.models import User


@shared_task
def send_notification(user_id, event_id, message):
    user = User.objects.get(id=user_id)
    event = Event.objects.get(id=event_id)
    send_mail(
        'Atualização de Evento',
        message,
        'noreply@eventmanagement.com',
        [user.email],
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
    user = User.objects.get(id=user_id)
    event = Event.objects.get(id=event_id)
    confirmation_url = f"http://localhost:8000/api/events/{event_id}/confirm_registration/"
    send_mail(
        'Confirmação de Inscrição',
        f'Clique no link para confirmar sua inscrição: {confirmation_url}',
        'noreply@eventmanagement.com',
        [user.email],
    )