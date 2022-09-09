from django.db import models
from django.contrib.auth.models import User


class Images(models.Model):
    
    dish_name = models.ForeignKey('dishes.Dishes', to_field='dish_name', on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    
    def __str__(self) -> str:
        return f'{self.dish_name}'

class Recipe(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    dish_name = models.ForeignKey('dishes.Dishes', to_field='dish_name', on_delete=models.CASCADE, null=True)
    ingredients = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ForeignKey(Images, on_delete=models.CASCADE, null=True)
    published = models.BooleanField(default=False, null=True)
    
    def __str__(self) -> str:
        return f'{self.dish_name}'
    
