from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Event, Registration
from notifications.tasks import send_notification


@receiver(post_save, sender=Event)
def send_update_notification(sender, instance, created, **kwargs):
    if not created:
        participants = instance.participants.all()
        for participant in participants:
            message = f'O evento "{instance.title}" foi atualizado. Nova data: {instance.date}, nova hora: {instance.time}.'
            send_notification.delay(user_id=participant.id, event_id=instance.id, message=message)


@receiver(post_save, sender=Event)
def send_cancellation_notification(sender, instance, **kwargs):
    if not instance.is_active:
        participants = instance.participants.all()
        for participant in participants:
            message = f'O evento "{instance.title}" foi cancelado.'
            send_notification.delay(user_id=participant.id, event_id=instance.id, message=message)


@receiver(post_save, sender=Registration)
def send_confirmation_notification(sender, instance, created, **kwargs):
    if created:
        message = f'Confirmação de inscrição para o evento "{instance.event.title}".'
        send_notification.delay(user_id=instance.participant.id, event_id=instance.event.id, message=message)
