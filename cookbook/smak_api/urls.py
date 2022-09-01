from django.urls import path
from . import views


urlpatterns = [
    path('', views.api_home, name='index'),
    path('all/', views.DishListApiView.as_view()),
    
]