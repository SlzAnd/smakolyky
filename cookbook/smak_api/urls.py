from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns



urlpatterns = [
    path('', views.api_home, name='home'),
    path('all/', views.DishesList.as_view(), name='all'),
    path('dishes/<str:dish_name>/', views.DishDetail.as_view(), name='dish'),
    
]

urlpatterns = format_suffix_patterns(urlpatterns)
