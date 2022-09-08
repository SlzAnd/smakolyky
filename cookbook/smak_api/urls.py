from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns



urlpatterns = [
    path('', view=views.api_home, name='home'),
    #path('all', view=views.DishesList.as_view(), name='all'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
