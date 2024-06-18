from django.test import TestCase
from rest_framework import request

# Crie um evento para teste no shell do Django
from events.models import Event
from django.utils import timezone

# Definindo um evento para uma semana à frente
event = Event.objects.create(
    title="Teste de Evento",
    description="Descrição do evento de teste.",
    date=timezone.now() + timezone.timedelta(weeks=1),
    time=timezone.now().time(),
    location="Local do evento",
    created_by=request.user
)
