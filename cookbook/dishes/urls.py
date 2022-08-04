from django.urls import path
from . import views


app_name = 'dishes'
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('about_us/', views.about_us, name='about_us'),
    path('how_to_use/', views.how_to_use, name='how_to_use'),
    path('add/', views.add, name='add'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('<int:id>/edit/', views.edit, name='edit'),
    path('recipe/<int:id>', views.recipe, name='recipe'),
    path('disheslist/', views.dishes_list, name='disheslist'),
    

]
