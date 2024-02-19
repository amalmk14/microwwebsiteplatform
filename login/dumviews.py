import email

from django.core.exceptions import ObjectDoesNotExist
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

# def signup(request):
#     if request.method == 'POST':
#         username=request.POST['username']
#         email=request.POST['email']
#         password1=request.POST['password1']
#         password2=request.POST['password2']
#
#         if password1 == password2:
#             if User.objects.filter(username=username).exists():
#                 messages.info(request,'Username Already Taken')
#                 return redirect('login:signup')
#             elif User.objects.filter(email=email).exists():
#                 messages.info(request,'Email Already Taken')
#                 return redirect('login:signup')
#             else:
#                 user=User.objects.create_user(username=username,password=password1,email=email)
#                 user.save();
#         else:
#             messages.info(request,'Password not matched')
#             return redirect('login:signup')
#         return redirect('login:signin')
#     return render(request,"signup.html")

# def signin(request):
    # if request.method == 'POST':
    #     username=request.POST['username']
    #     password=request.POST['password']
    #     user=auth.authenticate(username=username,password=password)
    #
    #     if user is not None:
    #         auth.login(request,user)
    #         return redirect('mainapp:home')
    #     else:
    #         messages.info(request,'Invalid Details')
    #         return redirect('login:signin')
    # return render(request,"signin.html")

# def logout(request):
#     auth.logout(request)
#     return redirect('login:signin')

# def forgot_password(request):
#     if request.method == 'POST':
#         email = request.POST.get('email', '').strip()
#
#         if not email:
#             messages.error(request, "Please enter your email.")
#             return redirect('login:forget')
#
#         elif User.objects.filter(email=email).exists():
#             OTP = random.randint(100000, 999999)
#             print(OTP)
#             user = User.objects.get(email=email)
#             subject = 'OTP for Forgott Password'
#             message = f'Hi {user.username},Your Forgott Password OTP is {OTP} Valid For 5 Minit'
#             email_from = settings.EMAIL_HOST_USER
#             recipient_list = {user.email}
#             send_mail( subject, message, email_from, recipient_list )
#             messages.info(request, "We will send an OTP to the email.")
#             return render(request, "forget.html", {"show_modal": True})
#         else:
#             messages.error(request, "Email is not registered on our site.")
#             return redirect('login:forget')
#     return render(request, "forget.html")


# def forgot_password(request):
#     if request.method == 'POST':
#         email = request.POST.get('email', '').strip()
#
#         if not email:
#             messages.error(request, "Please enter your email.")
#             return redirect('login:forget')
#
#         try:
#             user = User.objects.get(email=email)
#         except ObjectDoesNotExist:
#             messages.error(request, "Email is not registered on our site.")
#             return redirect('login:forget')
#
#         # Check if the user already has an OTP and if it's still valid
#         if user.otp and user.otp_expiration > timezone.now():
#             entered_otp = request.POST.get('otp', '')
#             if entered_otp == str(user.otp):
#                 # OTP is valid, you can reset the password here
#                 # For security, you should clear the OTP and its expiration in the user's record
#                 user.otp = None
#                 user.otp_expiration = None
#                 user.save()
#                 # Redirect to a password reset view or function
#                 return redirect('password_reset')  # Replace with the actual password reset view name
#             else:
#                 messages.error(request, "Invalid OTP. Please try again.")
#         else:
#             OTP = random.randint(100000, 999999)
#             user.otp = OTP
#             user.otp_expiration = timezone.now() + timezone.timedelta(minutes=5)
#             user.save()
#             subject = 'OTP for Forgot Password'
#             message = f'Hi {user.username}, Your Forgot Password OTP is {OTP} Valid For 5 Minutes'
#             email_from = settings.EMAIL_HOST_USER
#             recipient_list = [user.email]
#             send_mail(subject, message, email_from, recipient_list)
#             messages.info(request, "We will send an OTP to the email.")
#             return render(request, "forget.html", {"show_modal": True})
#
#     return render(request, "forget.html")