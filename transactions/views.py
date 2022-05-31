from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes

from .serializers import PaymentInfoSerializer, ReportSerializer
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
def save_report(request, pk):
    report_serializer = ReportSerializer(data={'user': pk})
    if report_serializer.is_valid():
        report_serializer.save()
    try:
        data = process_request(request.data)
        for payment in data:
            print(payment)
            # payment[]
            print(report_serializer.data)
            payment_serializer = PaymentInfoSerializer(data=payment, context={'report_id': 1})
            print(payment_serializer)
            if payment_serializer.is_valid():
                payment_serializer.save(report_id=report_serializer)
    except InvalidDateString:
        return Response('Bad request: "created_at" string(date-field) not valid.', status=status.HTTP_400_BAD_REQUEST)
    return Response(data, content_type='application/json')
