from django.db import models
from django.conf import settings

from users.models import CustomUser


class ActiveEventsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    organizer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    participants = models.ManyToManyField(CustomUser, through='Registration', related_name='events')

    def __str__(self):
        return self.title


class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    participant = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    confirmed = models.BooleanField(default=False)
    confirmed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('event', 'participant')

    def __str__(self):
        return f'{self.participant.username} - {self.event.title}'
