from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from events.models import Event


@swagger_auto_schema(
    method='get',
    operation_description="A detailed report of an event",
    responses={200: openapi.Response('response description', openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'event': openapi.Schema(type=openapi.TYPE_STRING, description='event title'),
            'participants': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'name': openapi.Schema(type=openapi.TYPE_STRING, description='participant name'),
                    'email': openapi.Schema(type=openapi.TYPE_STRING, description='participant email'),
                }
            ), description='list of participants')
        },
    ))},
)
@api_view(['GET'])
def event_report(request, event_id):
    event = Event.objects.get(id=event_id)
    participants = event.participants.all()
    data = {
        'event': event.title,
        'participants': [{'name': p.get_full_name(), 'email': p.email} for p in participants]
    }
    return Response(data)
