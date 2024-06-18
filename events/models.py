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
    active = models.BooleanField(default=True)
    organizer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    participants = models.ManyToManyField(CustomUser, through='Registration', related_name='events')

    def deactivate(self, *args, **kwargs):
        self.active = False
        self.save()

    def __str__(self):
        return self.title


class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'user')

    def __str__(self):
        return f'{self.user.username} - {self.event.title}'
