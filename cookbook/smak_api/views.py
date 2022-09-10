from django.http import Http404
from django.forms.models import model_to_dict
from django.contrib.auth.models import User

from rest_framework import status, permissions, generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from dishes.models import *
from .serializers import DishesSerializer, ImageSerializer, RecipeSerializer



@api_view(["GET"])
def api_home(request, *args, **kwargs):
    return Response({'message': 'Welcome to SmakolykyUA-API'})


"""
View for get all dishes and create new one
"""
class DishesList(APIView):
    
    #List all dishes [ GET ALL ]
    def get(self, request, format=None):
        dishes = Dishes.objects.all()
        serializer = DishesSerializer(dishes, many=True)
        print(serializer.data)
        return Response(serializer.data)

    # Create new dish [ POST ]
    def post(self, request, format=None):
        serializer = DishesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DishDetail(APIView):
    def get_object(self, dish_name):
        try:
            return Dishes.objects.get(dish_name=dish_name)
        except Dishes.DoesNotExist:
            raise Http404
    
    # Get one dish
    def get(self, request, dish_name, format=None):
        dish = self.get_object(dish_name)
        serializer = DishesSerializer(dish)
        return Response(serializer.data)
    
    def put(self, request, dish_name, format=None):
        dish = self.get_object (dish_name)
        serializer = DishesSerializer(dish, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, dish_name, format=None):
        dish = self.get_object(dish_name)
        dish.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)