from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


def get_image_filename(instance, filename):
    title = instance.images
    slug = slugify(title)
    return "%s-%s" % (slug, filename)


"""
Create the main model, named Dishes, for saving in the database
'user' in this model used for connecting with the User model (who created it)
"""
class Dishes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    dish_name = models.CharField(max_length=255, null=True)
    dish_url = models.CharField(max_length=255, null=True, blank=True)
    video_url = models.CharField(max_length=255, null=True, blank=True)    


"""
Create the model for saving dish images
The 'dish' used for connecting with the Dishes model(which dish corresponds to this image)
"""
class Dish_Images(models.Model):
    dish = models.ForeignKey(Dishes, on_delete=models.CASCADE, null=True)
    images = models.ImageField(null=True,blank=True, upload_to='images')


"""
Create the model for saving dish files
The 'dish' used for connecting with the Dishes model(which dish corresponds to this file)
"""
class Dish_Files(models.Model):
    dish = models.ForeignKey(Dishes, on_delete=models.CASCADE, null=True)
    files = models.FileField(null=True,blank=True, upload_to='files')

