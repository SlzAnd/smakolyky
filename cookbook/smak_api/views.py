from django.http import Http404
from django.forms.models import model_to_dict
from django.contrib.auth.models import User

from rest_framework import status, permissions, generics, mixins
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from dishes.models import *
from recipes.models import *
from .serializers import DishesSerializer, ImageSerializer, RecipeSerializer


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
    
    
""" 
RecipeList-view give possibility GET list of recipes and create(POST) new recipe 
"""
class RecipeList(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                generics.GenericAPIView):
    
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    

""" 
RecipeDetail-view give possibility GET one of recipes and edit(PUT), destroy(DELETE) one of them.
lookup-field by default = 'pk'. 
"""
class RecipeDetail(generics.RetrieveUpdateDestroyAPIView):
    
    # The field that should be used to for performing object lookup of individual model instances
    lookup_field = 'dish_name'
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    

class ImageList(generics.ListAPIView):
    
    queryset = Images.objects.all()
    serializer_class = ImageSerializer


class ImageCreate(APIView):

    def post(self, request, format=None):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageDetail(generics.RetrieveUpdateDestroyAPIView):
    
    # pk is default value for lookup_field
    lookup_field = 'pk'
    queryset = Images.objects.all()
    serializer_class = ImageSerializer
    
    