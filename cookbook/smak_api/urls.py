from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns



urlpatterns = [
    path('', views.DishesList.as_view(), name='all'),
    path('dishes/<str:dish_name>/', views.DishDetail.as_view(), name='dish'),
    
    path('recipes/', views.RecipeList.as_view()),
    path('recipes/<str:dish_name>/', views.RecipeDetail.as_view()),
    
    
    path('recipes/image/add/', views.ImageCreate.as_view()),
    path('recipes/image/<int:pk>/', views.ImageDetail.as_view()),
    path('recipes/image/all/', views.ImageList.as_view()),
    
    
]

urlpatterns = format_suffix_patterns(urlpatterns)
