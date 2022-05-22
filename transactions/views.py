from rest_framework.response import Response
from rest_framework.decorators import api_view


# Create your views here.
@api_view(['GET'])
def get_server_check(request):
    server_check_message = {'message': 'Server is ready for work.'}
    return Response(server_check_message)


@api_view(['POST'])
def generate_report(request):
    return Response(request.data)
