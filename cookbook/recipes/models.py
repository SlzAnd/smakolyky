from PIL import Image
from io import BytesIO

from django.db import models
from django.conf import settings
from django.core.files import File

User = settings.AUTH_USER_MODEL
class Images(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    image_name = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    thumbnail = models.ImageField(upload_to='images', null=True, blank=True)
    
    def __str__(self) -> str:
        return f'Image name: {self.image_name}'
    
    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''
    
    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                
                return 'http://127.0.0.1:8000' + self.thumbnail.url
            else:
                return ''
            
    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)
           
        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        
        thumbnail = File(thumb_io, name=image.name)
        
        return thumbnail

class Recipe(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    dish_name = models.CharField(max_length=255, null=True)
    ingredients = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ForeignKey(Images, on_delete=models.CASCADE, null=True)
    published = models.BooleanField(default=False, null=True)
    
    def __str__(self) -> str:
        return f'{self.dish_name}'
    
