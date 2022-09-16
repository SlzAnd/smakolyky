from urllib import request
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.reverse import reverse

from dishes.models import Dishes, Category
from recipes.models import Recipe, Images

class DishesSerializer(serializers.ModelSerializer):
    
    url = serializers.HyperlinkedIdentityField(
        view_name='dishes_detail',
        lookup_field = 'dish_name'
        )
    user = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Dishes
        fields = ['url',
                  'user',
                  'dish_name',
                  'dish_url',
                  'video_url',
                  'date_added',
                  'image',
                  'file',
                  'category',
                  ]
    
    # def get_edit_url(self, obj):
    #     request = self.context.get('request')
    #     if request is None:
    #         return None
    #     return reverse("dishes-edit", kwargs={"dish_name": obj.dish_name}, request=request)
    
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name',
                  'slug',
                  ]


class RecipeSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Recipe
        fields = ['user',
                  'dish_name',
                  'ingredients',
                  'description',
                  'created_at',
                  'image',
                  'published']
        
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['id',
                  'image_name',
                  'image',
                  'thumbnail']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'groups', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
            }
        
    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
        

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']