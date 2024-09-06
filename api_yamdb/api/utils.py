from rest_framework import status
from rest_framework.response import Response


def response_405_not_put():
    return Response(
        'PUT-запрос не предусмотрен',
        status=status.HTTP_405_METHOD_NOT_ALLOWED
    )
