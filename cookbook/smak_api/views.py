from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from rest_framework import status, permissions, generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from dishes.models import *
from .serializers import DishesSerializer



@api_view(["GET"])
def api_home(request, *args, **kwargs):
    return Response({'message': 'Welcome to SmakolykyUA-API'})


"""
View for get all dishes and create new one
"""
class DishesList(generics.ListCreateAPIView):
    queryset = Dishes.objects.all()
    serializer_class = DishesSerializer
    permission_classes = None

    #List all dishes
    def get(self, request, format=None):
        dishes = Dishes.objects.all()
        serializer = DishesSerializer(dishes, many=True)
        return Response(serializer.data)

    # Create new dish
    def post(self, request, format=None):
        serializer = DishesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)