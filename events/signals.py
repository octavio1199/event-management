from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail

from .models import Event, Registration
from notifications.models import Notification
from notifications.tasks import send_notification


@receiver(post_save, sender=Event)
def send_update_notification(sender, instance, created, **kwargs):
    if not created:
        participants = instance.participants.all()
        for participant in participants:
            message = f'O evento "{instance.title}" foi atualizado. Nova data: {instance.date}, nova hora: {instance.time}.'
            notification = Notification.objects.create(event=instance, user=participant, message=message)
            send_notification.delay(notification.id)


@receiver(post_delete, sender=Event)
def send_cancellation_notification(sender, instance, **kwargs):
    participants = instance.participants.all()
    for participant in participants:
        message = f'O evento "{instance.title}" foi cancelado.'
        notification = Notification.objects.create(event=instance, user=participant, message=message)
        send_notification.delay(notification.id)
