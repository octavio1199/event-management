from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Event, Registration
from .serializers import EventSerializer, RegistrationSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    @action(detail=True, methods=['post'])
    def register(self, request, pk=None):
        event = self.get_object()
        user = request.user
        registration = Registration.objects.create(event=event, user=user)
        serializer = RegistrationSerializer(registration)
        return Response(serializer.data)


class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    http_method_names = ['get', 'post', 'delete']

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        registration = self.get_object()
        registration.confirmed = True
        registration.save()
        return Response({'status': 'registration confirmed'}, status=status.HTTP_200_OK)
