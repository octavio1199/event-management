from django.core.mail import EmailMessage
from smtplib import SMTPException

from celery import shared_task
from django.db.backends.utils import logger

from reports.utils import generate_event_report


@shared_task
def generate_event_report_task(event_id, user_email):
    from events.models import Event
    event = Event.objects.get(id=event_id)
    participants = event.participants.all()
    file_path = generate_event_report(event, participants)

    email = EmailMessage(
        'EventManagement - Seu relatório está pronto',
        'Por favor, encontre o relatório do evento em anexo.',
        'noreply@eventmanagement.com',
        [user_email],
    )
    email.attach_file(file_path)
    print(f"Generated report for event {event_id}")
    try:
        print(f"Sending email to {user_email}")
        email.send()
    except SMTPException as e:
        print(f"Error sending email: {e}")
