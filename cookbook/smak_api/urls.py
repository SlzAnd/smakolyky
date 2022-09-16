from django.urls import path, include
from . import views

from rest_framework import authentication
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view


schema_view = swagger_get_schema_view(
    openapi.Info(
        title='SmakolykyUA API',
        default_version='1.0.8',
        description='API documentation of App'
    ),
    public=True,
    authentication_classes = [authentication.TokenAuthentication]
)


urlpatterns = [
    
    # Authorization-authentication end-points
    path('register/', views.RegisterAPIView.as_view(), name='user_create'),
    path('login/', views.LoginView.as_view(), name='user_login'),
    
    # Cookbook end-points
    path('', views.DishesList.as_view(), name='dishes_list'),
    path('dishes/<str:dish_name>/', views.DishDetail.as_view(), name='dishes_detail'),
    
    # Recipe end-points
    path('recipes/', views.RecipeList.as_view()),
    path('recipes/<str:dish_name>/', views.RecipeDetail.as_view()),
    
    # Images au-points
    path('recipes/image/add/', views.ImageCreate.as_view()),
    path('recipes/image/<int:pk>/', views.ImageDetail.as_view()),
    path('recipes/image/all/', views.ImageList.as_view()),
    
    path('swagger/schema/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
