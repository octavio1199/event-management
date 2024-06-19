from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.permissions import IsOwnerOrReadOnly
from .models import Event, Registration
from .serializers import EventSerializer, RegistrationSerializer
from notifications.tasks import send_confirmation_email


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def register(self, request, pk=None):
        event = self.get_object()
        user = request.user
        registration, created = Registration.objects.get_or_create(event=event, user=user)
        if created:
            send_confirmation_email.delay(user.id, registration.id)
        serializer = RegistrationSerializer(registration)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsOwnerOrReadOnly])
    def confirm_registration(self, request, pk=None):
        registration = Registration.objects.get(event__id=pk, user=request.user)
        registration.confirmed = True
        registration.confirmed_at = timezone.now()
        registration.save()
        return Response({'status': 'confirmed'})

    @action(detail=True, methods=['put'])
    def cancel_registration(self, request, pk=None, ):
        registration = Registration.objects.get(event__id=pk, user=request.user)
        registration.is_active = False
        registration.save()
        return Response({'status': 'canceled'})
