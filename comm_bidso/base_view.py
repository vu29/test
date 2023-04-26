"""
Base View for the project
"""

from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


class BaseView(APIView):
    "BaseView class for other views to inherit"

    renderer_classes = [JSONRenderer]

    def http_response(self, status, message, response, status_code):
        return Response(
            {"status": status, "msg": message, "response": response}, status=status_code
        )
