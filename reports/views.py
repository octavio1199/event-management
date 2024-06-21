from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from events.models import Event
from reports.tasks import generate_event_report_task


@swagger_auto_schema(
    method='get',
    operation_description="A detailed report of an event",
    responses={
        200: openapi.Response('The report is being generated and will be sent to your email shortly.', openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Response detail'),
            },
        )),
        403: openapi.Response('You do not have permission to perform this action.', openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Response detail'),
            },
        )),
        404: openapi.Response('Event not found.', openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Response detail'),
            },
        )),
    },
)
@api_view(['GET'])
def event_report(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return Response({'detail': 'Event not found.'}, status=status.HTTP_404_NOT_FOUND)

    if not (request.user == event.organizer or request.user.is_staff):
        return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

    generate_event_report_task.delay(event_id, request.user.email)

    return Response({'detail': 'O relatório está sendo gerado e será enviado para o seu email em breve.'})
