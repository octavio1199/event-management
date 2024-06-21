from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.backends.utils import logger

from users.permissions import IsOwnerOrReadOnly
from .models import Event, Registration
from .serializers import EventSerializerResponse, RegistrationSerializer, EventSerializerRequest


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class_req = EventSerializerRequest
    serializer_class = EventSerializerResponse
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]
    pagination_class = PageNumberPagination

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class_req(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(organizer=request.user)
        print(10, f'Event created by {request.user}')
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class_req(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def register(self, request, pk=None):
        event = self.get_object()
        user = request.user
        registration, created = Registration.objects.get_or_create(event=event, participant=user)
        serializer = RegistrationSerializer(registration)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsOwnerOrReadOnly])
    def confirm_registration(self, request, pk=None):
        registration = Registration.objects.get(event__id=pk, participant=request.user)
        registration.confirmed = True
        registration.confirmed_at = timezone.now()
        registration.save()
        return Response({'status': 'confirmed'})

    @action(detail=True, methods=['put'])
    def cancel_registration(self, request, pk=None, ):
        registration = Registration.objects.get(event__id=pk, participant=request.user)
        registration.confirmed = False
        registration.is_active = False
        registration.save()
        return Response({'status': 'canceled'})
