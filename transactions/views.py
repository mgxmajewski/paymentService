from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import PayByLinkSerializer


# Create your views here.
@api_view(['GET'])
def get_server_check(request):
    server_check_message = {'message': 'Server is ready for work.'}
    return Response(server_check_message)


@api_view(['POST'])
def generate_report(request):
    print(request)
    new_report_serializer = PayByLinkSerializer(data=request.data)
    if new_report_serializer.is_valid():
        pass

    return Response(new_report_serializer.data)
