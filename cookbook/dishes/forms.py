from django.forms import ModelForm, TextInput, ClearableFileInput, modelformset_factory, BaseFormSet
from .models import Dishes, Dish_Images, Dish_Files
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields = ['username', 'email', 'password1', 'password2']
        
class AddDishForm(ModelForm):
    class Meta:
        model = Dishes
        fields = ['dish_name', 'dish_url', 'video_url']
        widgets = {
            'dish_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введіть назву',
                'label': ''
                 }),
            'dish_url': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Вставте посилання',
                     'label': '',
                     'blank': True
                      }),
            'video_url': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Вставте посилання на відео',
                     'label': '',
                     'blank': True }
                )              
            }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""

class DishImageForm(ModelForm):
    class Meta:
        model = Dish_Images
        fields = ['images']
        widgets = {
            'images': ClearableFileInput(
                attrs={
                    'class': 'form-control',
                    #'multiple': True
                    })
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""

class DishFileForm(ModelForm):
    class Meta:
        model = Dish_Files
        fields = ['files']
        widgets = {
            'files': ClearableFileInput(
                attrs={
                    'class': 'form-control',
                    #'multiple': True
                    })
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""
