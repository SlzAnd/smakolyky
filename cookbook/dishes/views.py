from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Dishes, Dish_Images, Dish_Files
from .forms import AddDishForm, DishImageForm, DishFileForm, CreateUserForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

import re


# Create your views here.
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
            #'help_text': help_text
        }
        return render(request,'dishes/register.html', context)

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

def index(request):
    return render(request, 'dishes/index.html', {})

def about_us(request):
    return render(request,'dishes/about_us.html', {})

def how_to_use(request):
    return render(request,'dishes/how_to_use.html', {})

def logoutUser(request):
    logout(request)
    return redirect('dishes:login')


@login_required(login_url='dishes:login')
def dishes_list(request):
    user = request.user
    dishes = Dishes.objects.filter(user=user).values()
    template = loader.get_template('dishes/dishes_list.html')
    context = {
        'dishes': dishes,
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='dishes:login')
def add(request):
    if request.method == 'POST':
        name = AddDishForm(request.POST)
        user = request.user
        dishname = request.POST.get('dish_name')
        dishurl = request.POST.get('dish_url')
        videourl = request.POST.get('video_url')
        image_list = request.FILES.getlist('images')
        file_list = request.FILES.getlist('files')
        if name['dish_name'] != None:
            dish_name = Dishes.objects.create(dish_name = dishname, dish_url = dishurl, video_url = videourl, user=user)
        else:
            dish_name = None
        for image in image_list:
            img = Dish_Images.objects.create(images = image, dish = dish_name)
        for file in file_list:
            f = Dish_Files.objects.create(files = file, dish = dish_name)
        return redirect('dishes:disheslist')
    else:
        name = AddDishForm()
        image = DishImageForm()
        file = DishFileForm()
    return render(request, 'dishes/add.html', { 'form' : name, 'images_form': image, 'files_form': file })


def delete(request, id):
    dish = Dishes.objects.get(id=id)
    dish.delete()
    return HttpResponseRedirect(reverse('dishes:disheslist'))


@login_required(login_url='dishes:login')
def edit(request, id):
    dish = Dishes.objects.get(id=id)    
    image_list = Dish_Images.objects.filter(dish=dish)
    file_list = Dish_Files.objects.filter(dish=dish)
    
    if request.method == 'POST':
        form = AddDishForm(request.POST, instance = dish)
        if len(image_list) == 0:
            new_img = request.FILES.get('images')
            Dish_Images.objects.create(images = new_img, dish = dish)
        else:
            images = Dish_Images.objects.get(dish=dish)
            image_form = DishImageForm(request.POST, request.FILES, instance = images)
            if image_form.is_valid:
                image_form.save()
        if len(file_list) == 0:
            file = request.FILES.get('files')
            Dish_Files.objects.create(files=file, dish=dish)
        else:            
            file = Dish_Files.objects.get(dish=dish)            
            file_form = DishFileForm(request.POST, request.FILES, instance=file)
            if file_form.is_valid:
                file_form.save()  
        if form.is_valid:                     
                form.save()
                  
        return redirect('dishes:disheslist')
    else:        
        form = AddDishForm(instance=dish)
        if len(image_list) == 0:
            image_form = DishImageForm()
        else:
            images = Dish_Images.objects.get(dish=dish)            
            image_form = DishImageForm(instance=images)
        if len(file_list) == 0:
            file_form = DishFileForm()
        else:
            file = Dish_Files.objects.get(dish=dish)
            file_form = DishFileForm(instance=file)
                   
    return render(request, 'dishes/edit.html', {'form': form,'image_list': image_list, 'image_form': image_form, 'file_form': file_form })


@login_required(login_url='dishes:login')
def recipe(request, id):
    dish = Dishes.objects.get(id=id)
    try:
        image = Dish_Images.objects.get(dish=dish)        
    except ObjectDoesNotExist:
        image = 0
    try:
        file = Dish_Files.objects.get(dish=dish)
    except ObjectDoesNotExist:
        file = 0

    if Dish_Images.objects.filter(dish=dish, images__exact='').count() > 0:
        images = 0
    else:
        images = image
    if Dish_Files.objects.filter(dish=dish, files__exact='').count() > 0:
        files = 0
    else:
        files = file

    return render(request,'dishes/recipe.html',{'dish': dish, 'images': images, 'files': files})
