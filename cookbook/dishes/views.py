from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Dishes
from .forms import AddDishForm, CreateUserForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
import requests
from getpass import getpass
import re


"""
Register View.
"""
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('dishes:disheslist')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            user = request.POST.get('user')
            if form.is_valid:
                try:
                    form.save()
                    user = form.cleaned_data.get('username')
                    messages.success(request, 'Account was created for ' + user)
                    return redirect('dishes:login')                    
                except ValueError:
                    pass
                
        context = {
            'form':form,
        }
        return render(request,'dishes/register.html', context)


"""
Login View.
"""
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('dishes:disheslist')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            user = authenticate(request, username = username, password = password)

            if user is not None:
                login(request, user)
                return redirect('dishes:disheslist')
            else:
                messages.info(request, 'Username Or Password is incorrect')
        context = {
        }
        return render(request,'dishes/login.html', context)


"""
Main Page View. Render template only
"""
def index(request):
    return render(request, 'dishes/index.html', {})


"""
About Us Page View. Render template only
"""
def about_us(request):
    return render(request,'dishes/about_us.html', {})


"""
How to use Page View. Render template only
"""
def how_to_use(request):
    return render(request,'dishes/how_to_use.html', {})


"""
Log OUT View.
"""
def logoutUser(request):
    logout(request)
    return redirect('dishes:login')


"""
List with all user's dishes.
"""
@login_required(login_url='dishes:login')
def dishes_list(request):
    user = request.user
    dishes = Dishes.objects.filter(user=user).values()
    template = loader.get_template('dishes/dishes_list.html')
    context = {
        'dishes': dishes,
    }
    return HttpResponse(template.render(context, request))
    # user = request.user
    # response = requests.get('http://127.0.0.1:8000/api/all', auth=(user.username, '784512Sa'))
    # dishes = response.json()
    # print(dishes)
    
    # return render(request, 'dishes/dishes_list.html', dishes)


"""
View for adding new dish to your list.
"""
@login_required(login_url='dishes:login')
def add(request):
    if request.method == 'POST':
        name = AddDishForm(request.POST)
        user = request.user
        dishname = request.POST.get('dish_name')
        dishurl = request.POST.get('dish_url')
        videourl = request.POST.get('video_url')
        image = request.FILES.get('image')
        file = request.FILES.get('file')
        if name['dish_name'] != None:
            Dishes.objects.create(dish_name = dishname, dish_url = dishurl,
                                              video_url = videourl, image=image, file=file, user=user)
        return redirect('dishes:disheslist')
    else:
        form = AddDishForm()
    return render(request, 'dishes/add.html', {'form':form})


"""
View for deleting dish from your list.
"""
def delete(request, id):
    dish = Dishes.objects.get(id=id)
    dish.delete()
    return HttpResponseRedirect(reverse('dishes:disheslist'))


"""
View for editing dish in your list.
"""
@login_required(login_url='dishes:login')
def edit(request, id):
    dish = Dishes.objects.get(id=id)    
    
    if request.method == 'POST':
        form = AddDishForm(request.POST, request.FILES, instance = dish)
        
        if form.is_valid:                     
                form.save()
                  
        return redirect('dishes:disheslist')
    else:        
        form = AddDishForm(instance=dish)
                          
    return render(request, 'dishes/edit.html', {'form':form})



"""
View for looking a dish from your list. Render new page with accordion(Image, Video, URL, File)
"""
@login_required(login_url='dishes:login')
def recipe(request, id):
    dish = Dishes.objects.get(id=id)
        
    return render(request,'dishes/recipe.html',{'dish':dish})
