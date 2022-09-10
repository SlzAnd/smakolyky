from django.contrib.auth.models import User, Group
from rest_framework import serializers

from dishes.models import Dishes, Category
from recipes.models import Recipe, Images

class DishesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dishes
        fields = ['user',
                  'dish_name',
                  'dish_url',
                  'video_url',
                  'date_added',
                  'image',
                  'file',
                  'category',
                  ]
        
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name',
                  'slug',
                  ]


class RecipeSerializer(serializers.ModelSerializer):
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
        fields = ['dish_name',
                  'image']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']