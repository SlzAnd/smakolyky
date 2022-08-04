from django.contrib import admin
from .models import Dishes, Dish_Images, Dish_Files
# Register your models here.

admin.site.register(Dishes)
admin.site.register(Dish_Images)
admin.site.register(Dish_Files)