from dataclasses import field
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from dishes.models import Dishes

class DishesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dishes
        fields = ['user',
                  'dish_name',
                  'dish_url',
                  'video_url',
                  ]

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']