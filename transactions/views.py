from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from .services import process_request, InvalidDateString


# Create your views here.
@api_view(['GET'])
def get_server_check(request):
    server_check_message = {'message': 'Server is ready for work.'}
    return Response(server_check_message)


@api_view(['POST'])
# @renderer_classes([JSONRenderer])
def generate_report(request):
    try:
        report = process_request(request.data)
    except InvalidDateString:
        return Response('Bad request: "created_at" string(date-field) not valid.', status=status.HTTP_400_BAD_REQUEST)
    return Response(report, content_type='application/json')


@api_view(['POST'])
# @renderer_classes([JSONRenderer])
def save_report(request):
    try:
        report = process_request(request.data)
    except InvalidDateString:
        return Response('Bad request: "created_at" string(date-field) not valid.', status=status.HTTP_400_BAD_REQUEST)
    return Response(report, content_type='application/json')
