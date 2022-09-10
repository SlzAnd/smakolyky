from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


def get_image_filename(instance, filename):
    title = instance.images
    img_slug = slugify(title)
    return "%s-%s" % (img_slug, filename)


"""
Create the model for categories of dishes + recipes
"""
class Category(models.Model):
    
    name = models.CharField(max_length=255, null=True, unique=True)
    slug = models.SlugField()
    
    class Meta:
        ordering = ('name',)
        
    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return f'/{self.slug}/'



"""
Create the main model, named Dishes, for saving in the database
'user' in this model used for connecting with the User model (who created it)
"""
class Dishes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    dish_name = models.CharField(max_length=255, null=True, unique=True)
    dish_url = models.CharField(max_length=255, null=True, blank=True)
    video_url = models.CharField(max_length=255, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True, blank=True, upload_to='images')
    file = models.FileField(null=True, blank=True, upload_to='files')
    category = models.ForeignKey(Category, to_field='name', verbose_name='category', on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return f'ID: {self.id} | User: {self.user} | Dish: {self.dish_name}'

    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        else:
            return ''

    


      
