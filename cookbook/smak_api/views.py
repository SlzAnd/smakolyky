from django.http import JsonResponse
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view
from rest_framework.response import Response
from dishes.models import *
from .serializers import DishesSerializer

@api_view(["GET"])
def api_home(request, *args, **kwargs):
    serializer = DishesSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        return Response(serializer.data)
    return Response({"invalid":"not good data"}, status=400)