from urllib import request
from django.http import Http404
from django.forms.models import model_to_dict
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from rest_framework import status, permissions, generics, mixins, authentication
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
# from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework.authtoken.models import Token
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_simplejwt.authentication import JWTAuthentication

from knox.auth import AuthToken

from dishes.models import *
from recipes.models import *
from .serializers import (DishesSerializer, ImageSerializer,
                          RecipeSerializer, UserSerializer)
from .mixins import UserQuerySetMixin
from .authentication import TokenAuthentication


class RegisterAPIView(generics.GenericAPIView):
    
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        })


class LoginView(generics.GenericAPIView):
    serializer_class = AuthTokenSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        _, token = AuthToken.objects.create(user)
        
        login(request, user)
        
        return Response({
            'user_info': {
                'id': user.id,
                'username': user.username,                
            },
            'token': token
        })


"""
View for get all dishes and create new one
"""
class DishesList(APIView):
    
    permission_classes = [permissions.IsAuthenticated]
    #authentication_classes = [authentication.TokenAuthentication]
       
    #List all dishes [ GET ALL ]
    def get(self, request, format=None):
        dishes = Dishes.objects.filter(user=request.user).all()
        serializer = DishesSerializer(dishes, many=True, context={'request': request})
        print(serializer.data)
        return Response(serializer.data)

    # Create new dish [ POST ]
    def post(self, request, format=None):
        print(request.user)
        serializer = DishesSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DishDetail(APIView):
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self, user, dish_name):
        try:
            return Dishes.objects.filter(user=user).get(dish_name=dish_name)
        except Dishes.DoesNotExist:
            raise Http404
    
    # Get one dish
    def get(self, request, dish_name, format=None):
        dish = self.get_object(request.user, dish_name)
        serializer = DishesSerializer(dish, context={'request': request})
        return Response(serializer.data)
    
    def put(self, request, dish_name, format=None):
        dish = self.get_object (request.user, dish_name)
        serializer = DishesSerializer(dish, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, dish_name, format=None):
        dish = self.get_object(request.user, dish_name)
        dish.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
""" 
RecipeList-view give possibility GET list of recipes and create(POST) new recipe 
"""

class RecipeList(UserQuerySetMixin,
                generics.ListCreateAPIView):
  
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
    
""" 
RecipeDetail-view give possibility GET one of recipes and edit(PUT), destroy(DELETE) one of them.
lookup-field by default = 'pk', but we use dish name.
"""
class RecipeDetail(UserQuerySetMixin,
                   generics.RetrieveUpdateDestroyAPIView):
    
    permission_classes = [permissions.IsAuthenticated]
    
    # The field that should be used to for performing object lookup of individual model instances
    lookup_field = 'dish_name'
     
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class ImageList(UserQuerySetMixin, generics.ListAPIView):
    
    permission_classes = [permissions.IsAuthenticated]
    
    queryset = Images.objects.all()
    serializer_class = ImageSerializer


class ImageCreate(APIView):

    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, format=None):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageDetail(UserQuerySetMixin, generics.RetrieveUpdateDestroyAPIView):
    
    permission_classes = [permissions.IsAuthenticated]
    
    # pk is default value for lookup_field
    lookup_field = 'pk'
    queryset = Images.objects.all()
    serializer_class = ImageSerializer
    