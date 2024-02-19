import email

from django.core.exceptions import ObjectDoesNotExist
import re
from django.shortcuts import render, redirect,HttpResponseRedirect
from django.contrib import messages,auth
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import *
from django.core.mail import send_mail
from django.conf import settings
import random
from django.utils import timezone

# Create your views here.

def profile(request):
    # name = request.session['username']
    name = request.session.get('username')
    if name:
        profile_object = Profiles.objects.get(name=name)
        email = profile_object.email
        phone = profile_object.phone
        country = profile_object.country

    if request.method == 'POST':
        phone = request.POST['phone']
        country = request.POST['country']

        profile_object.phone = phone
        profile_object.country = country
        profile_object.save()
        return redirect('login:profile')
    return render(request,'profile/profile.html',{'name':name,'email':email,'phone':phone,'country':country})

def profile_password(request):
    name = request.session.get('username')
    if name:
        profile_object = Profiles.objects.get(name=name)

    if request.method == 'POST':
        password = request.POST['password']
        new_password1 = request.POST['new_password1']
        new_password2 = request.POST['new_password2']

        if new_password1 == new_password2:
            if profile_object.password == password:  # Check if old password matches
                profile_object.password = new_password1  # Assign the new password
                profile_object.save()  # Save the changes to the database
                messages.info(request, 'Password changed successfully')
                return redirect('login:profile')
            else:
                messages.info(request, 'Old password not matched')
                return redirect('login:profile')
        else:
            messages.info(request, 'New Password and Confirm Password are not matched')
            return redirect('login:profile')


def bill(request):
    return render(request,"profile/bill.html")

def security(request):
    return render(request,"profile/security.html")

def signup(request):
    if request.method == 'POST':
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']

        password_pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$')

        if not password_pattern.match(password1):
            messages.info(request,
                          'Password must contain at least one uppercase letter, one lowercase letter, one number, one special character, and be at least 8 characters long.')
            return redirect('login:signup')

        if password1 == password2:
            if Profiles.objects.filter(name=username).exists():
                messages.info(request,'Username Already Taken')
                return redirect('login:signup')
            elif Profiles.objects.filter(email=email).exists():
                messages.info(request,'Email Already Taken')
                return redirect('login:signup')
            else:
                user = Profiles(name=username,password=password1,email=email)
                user.save();
        else:
            messages.info(request,'Password not matched')
            return redirect('login:signup')
        return redirect('login:signin')
    return render(request,"signup.html")

def logout(request):
    request.session['is_logged_in'] = False
    return render(request,"home.html")


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        users = Profiles.objects.filter(name=username, password=password)
        # if not username or not password:
        #     error_message = "Both username and password are required."
        #     return render(request, 'signin.html', {'error_message': error_message})

        if users.exists():
            request.session['username'] = username
            request.session['is_logged_in'] = True
            return HttpResponseRedirect(reverse('mainapp:home') + f'?username={username}')
            # return redirect('mainapp:home')
            # return render(request, 'home.html', {})  # Redirect to 'userhome' after successful login
        else:
            messages.info(request,"Invalid username or password.")
            return redirect("login:signin")
    return render(request, 'signin.html')


