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

from knox.auth import AuthToken

from dishes.models import *
from recipes.models import *
from .serializers import (DishesSerializer, ImageSerializer,
                          RecipeSerializer, UserSerializer)
from .mixins import UserQuerySetMixin
from .authentication import TokenAuthentication

from drf_yasg.utils import swagger_auto_schema

class RegisterAPIView(generics.GenericAPIView):
    
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
            tags=['Create User'],
            responses={
                '200': "Successfully created user",
                '400': "Bad Request"
            },
            security=[],
            operation_id='Register New User',
            operation_description='This endpoint creates a new user'
        )
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
    
    @swagger_auto_schema(
        tags=['Login'],
        security=[],
        operation_id='Login',
        operation_description='This endpoint authenticate user. In response you get Auth Token'
    )
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
    @swagger_auto_schema(
        tags=['Dishes'],
        responses={
            '200': "OK",
            '400': "Bad Request"
            },
        security=[],
        operation_id='GET All Dishes',
        operation_description='This endpoint response list of all Dishes. Filtered by auth user'
        )
    def get(self, request, format=None):
        dishes = Dishes.objects.filter(user=request.user).all()
        serializer = DishesSerializer(dishes, many=True, context={'request': request})
        print(serializer.data)
        return Response(serializer.data)

    # Create new dish [ POST ]
    @swagger_auto_schema(
        tags=['Dishes'],
        responses={
            '201': "New Dish successfully created",
            '400': "Bad Request"
            },
        security=[],
        operation_id='Create a New Dish',
        operation_description='This endpoint creates a new dish. Used auth user'
    )
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
    
    # Get one dish by dish_name [GET]
    @swagger_auto_schema(
        tags=['Dishes'],
        responses={
            '200': "OK",
            '400': "Bad Request"
            },
        security=[],
        operation_id='Get One Dish',
        operation_description='This endpoint retrieve one dish by name. Used auth user'
    )
    def get(self, request, dish_name, format=None):
        dish = self.get_object(request.user, dish_name)
        serializer = DishesSerializer(dish, context={'request': request})
        return Response(serializer.data)
    
    # Update One Dish by dish_name [PUT]
    @swagger_auto_schema(
        tags=['Dishes'],
        responses={
            '200': "OK",
            '400': "Bad Request"
            },
        security=[],
        operation_id='Edit One Dish',
        operation_description='This endpoint edit one dish by name. Used auth user'
    )
    def put(self, request, dish_name, format=None):
        dish = self.get_object (request.user, dish_name)
        serializer = DishesSerializer(dish, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete One Dish by dish_name [DELETE]
    @swagger_auto_schema(
        tags=['Dishes'],
        responses={
            '204': "Successfully deleted. No Content!",
            '400': "Bad Request"
            },
        security=[],
        operation_id='Delete One Dish',
        operation_description='This endpoint delete one dish by name. Used auth user'
    )
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
    
    # Get All Recipes [GET ALL]
    @swagger_auto_schema(
        tags=['Recipes'],
        responses={
            '200': "OK",
            '400': "Bad Request"
            },
        security=[],
        operation_id='Get All Recipes',
        operation_description='This endpoint response list of all Recipes. Filtered by auth user.'
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    
    # Create New Recipe [POST]
    @swagger_auto_schema(
        tags=['Recipes'],
        responses={
            '201': "Successfully created",
            '400': "Bad Request"
            },
        security=[],
        operation_id='Create New Recipe',
        operation_description='This endpoint creates a new Recipe. Used auth user.'
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    
    
    
    
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

    # Get One Recipe [GET]
    @swagger_auto_schema(
        tags=['Recipes'],
        responses={
            '200': "OK",
            '400': "Bad Request"
            },
        security=[],
        operation_id='Get One Recipe',
        operation_description='This endpoint retrieve one Recipe by dish_name. Used auth user.'
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    # Edit One Recipe [PUT]
    @swagger_auto_schema(
        tags=['Recipes'],
        responses={
            '200': "OK",
            '400': "Bad Request"
            },
        security=[],
        operation_id='Edit One Recipe',
        operation_description='This endpoint update one Recipe by dish_name. Used auth user.'
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    # Partial Update One Recipe by PK [PATCH]
    @swagger_auto_schema(
        tags=['Recipes'],
        responses={
            '200': "OK",
            '400': "Bad Request"
            },
        security=[],
        operation_id='Partial Update One Recipe',
        operation_description='This endpoint partial update one Recipe. Used auth user.'
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    # Delete One Recipe [DELETE]
    @swagger_auto_schema(
        tags=['Recipes'],
        responses={
            '204': "Successfully deleted. No content",
            '400': "Bad Request"
            },
        security=[],
        operation_id='Delete One Recipe',
        operation_description='This endpoint delete one Recipe by dish_name. Used auth user.'
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class ImageList(UserQuerySetMixin, generics.ListAPIView):
    
    permission_classes = [permissions.IsAuthenticated]
    
    queryset = Images.objects.all()
    serializer_class = ImageSerializer

    # Get All Images for user's Recipes [GET ALL]
    @swagger_auto_schema(
        tags=['Images'],
        responses={
            '200': "OK",
            '400': "Bad Request"
            },
        security=[],
        operation_id='Get All Images',
        operation_description='This endpoint response list of all user`s Images. Filtered by auth user.'
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class ImageCreate(APIView):

    permission_classes = [permissions.IsAuthenticated]
    
    # Create New Image for user's Recipe [POST]
    @swagger_auto_schema(
        tags=['Images'],
        responses={
            '201': "Successfully created",
            '400': "Bad Request"
            },
        security=[],
        operation_id='Create New Image',
        operation_description='This endpoint creates new Image. Used auth user.'
    )
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
    
    # Get One Image by PK [GET]
    @swagger_auto_schema(
        tags=['Images'],
        responses={
            '200': "OK",
            '400': "Bad Request"
            },
        security=[],
        operation_id='Get One Image',
        operation_description='This endpoint retrieve one Image. Used auth user.'
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    # Update One Image by PK [ PUT]
    @swagger_auto_schema(
        tags=['Images'],
        responses={
            '200': "OK",
            '400': "Bad Request"
            },
        security=[],
        operation_id='Edit One Image',
        operation_description='This endpoint update one Image. Used auth user.'
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    # Partial Update One Image by PK [PATCH]
    @swagger_auto_schema(
        tags=['Images'],
        responses={
            '200': "OK",
            '400': "Bad Request"
            },
        security=[],
        operation_id='Partial Update One Image',
        operation_description='This endpoint partial update one Image. Used auth user.'
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    # Delete One Image by PK [DELETE]
    @swagger_auto_schema(
        tags=['Images'],
        responses={
            '204': "Successfully deleted. No Content",
            '400': "Bad Request"
            },
        security=[],
        operation_id='Delete One Image',
        operation_description='This endpoint delete one Image. Used auth user.'
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)