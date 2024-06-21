from django.db import models
from django.conf import settings
from events.models import Event


class Notification(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    sent = models.BooleanField(default=False)

    def __str__(self):
        return f'Notification for {self.receiver.email} about {self.event.title}'
