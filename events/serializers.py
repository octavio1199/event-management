from django.utils.datetime_safe import date
from rest_framework import serializers
from .models import Event, Registration


class EventSerializerResponse(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'time', 'location']


class EventSerializerRequest(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'time', 'location']

    def validate_date(self, value):
        if value <= date.today():
            raise serializers.ValidationError("The date of the event must be greater than the current date.")
        return value


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ['id', 'event', 'participant', 'registered_at']
