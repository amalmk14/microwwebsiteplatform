from django.shortcuts import render, redirect,HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.core.mail import send_mail
from django_otp.plugins.otp_email.models import EmailDevice
from django.contrib.auth import get_user_model
from django.conf import settings
import os
import zipfile
from django.core.paginator import Paginator, EmptyPage, InvalidPage

# Create your views here.
def logout(request):
    request.session['is_logged_in'] = False
    return render(request,"index.html")



def index(request):
    uid=request.session['username']
    temps = TemplateCard.objects.all().filter()
    paginator = Paginator(temps, 6)
    try:
        page = int(request.GET.get('page', "1"))
    except:
        page = 1
    try:
        temps = paginator.page(page)
    except (EmptyPage, InvalidPage):
        temps = paginator.page(paginator.num_pages)

    premiums = PremiumCard.objects.all().filter()
    paginators = Paginator(premiums, 8)
    try:
        pages = int(request.GET.get('page', "1"))
    except:
        pages = 1
    try:
        premiums = paginators.page(pages)
    except (EmptyPage, InvalidPage):
        premiums = paginators.page(paginator.num_pages)
    return render(request,"index.html",{'temps':temps,'premiums':premiums,'username':uid,})
    


def k(request):
    return render(request,"k.html")

# def login(request):
#     if request.method == 'POST':
#         # Check if the form data contains a 'password1' field to distinguish between registration and login.
#         if 'password1' in request.POST:
#             # Registration
            
#             if form.is_valid():
#                 password1 = form.cleaned_data['password1']
#                 password2 = form.cleaned_data['password2']
#                 if password1 == password2:
#                     form.save()
#                     username = form.cleaned_data['username']
#                     password = form.cleaned_data['password1']
#                     user = authenticate(username=username, password=password)
#                     login(request, user)
#                     return redirect('dashboard')
#                 else:
#                     # Passwords don't match, show an error message
#                     form.add_error('password2', 'Passwords do not match.')
#         else:
#             # Login
#             username = request.POST['username']
#             password = request.POST['password']
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('dashboard')
#             else:
#                 # Handle invalid login
#                 pass
#     else:
#        pass
#     return render(request, 'registration.html', {'form': form})



# def login(request):
#     return render(request,"login.html")



def login(request):  
    error_message = ""         
    if request.method == 'POST':
            print('hghjghjghgh')
            username = request.POST['name']
            password = request.POST['pass'] 
            
           
            users = Logins.objects.filter(username=username,password=password)
            if not username or not password:
                error_message = "Both username and password are required."
                return render(request, 'login.html',{'error_message': error_message})
                
            elif users.exists():
                print('exits')
                request.session['username']=username
                request.session['is_logged_in'] = True
                return render(request,'index.html',{})  # Redirect to 'userhome' after successful login
            else:
                # Handle invalid login
                error_message = "Invalid username or password."
                HttpResponseRedirect("login")
    return render(request, 'login.html',{'error_message': error_message})

def register(request):
        
        error_message = ""  # Initialize error_message
        if request.method == 'POST':
            # Check if the form data contains a 'reregpass' field to distinguish between registration and login.
            if all(field in request.POST for field in ['regname', 'regpass', 'reregpass']):
                # Registration
                username = request.POST['regname']
                password1 = request.POST['regpass']
                password2 = request.POST['reregpass']
                # gmail=request.POST['gmail']

                if password1 == password2:
                    # Check if the username is available
                    if Logins.objects.filter(username=username).exists():
                        # Handle username already exists
                        error_message = "Username already exists."
                        
                    else:
                        # Create a new user
                        Logins(username=username, password=password1,).save()
                        # user = get_user_model().objects.get(username=username)
                        # device = TOTPDevice.objects.create(user=user, confirmed=True)
                        # device.save()
                        # user.otp_secret = device.config_url()
                        # user.save()
                    
                    # Send the OTP to the user's email (you may need to customize this)
                        # send_email_otp(user)
                        # login(request)
                        # return HttpResponseRedirect('login')
                else:
                    error_message = "Passwords do not match."
        return render(request, 'login.html',{'error_message': error_message})            
                    # You can handle this in your HTML template



@login_required
def userhome(request):
    return render(request,"userhome.html")



# def login(request):
#     error_message = ""  # Initialize error_message
#     if request.method == 'POST':
 
#             username = request.POST['name']
#             password = request.POST['pass'] 
#             print(username)
#             print(password)   
#             users = Logins.objects.filter(username=username,password=password)
#             if users.exists():
#                 print('exits')
#                 return HttpResponseRedirect('userhome')  # Redirect to 'userhome' after successful login
#             else:
#                 # Handle invalid login
#                 error_message = "Invalid username or password."
#                 print("ckvjjv")
#     return render(request, 'login.html',{'error_message': error_message})



def send_email_otp(user):
    totp_device = TOTPDevice.objects.get(user=user)
    otp_token = totp_device.generate_token()

    subject = "Your OTP Code"
    message = f"Your OTP code is: {otp_token}"

    # Use the email settings defined in your Django project's settings.py
    from_email = "gokulmohan1348@gmail.com"  
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)







def temp_view(request, template_card_id):
    try:
        # Get the TemplateCard object by ID
        template_card = TemplateCard.objects.get(id=template_card_id)

        # Extract necessary information from the TemplateCard
        zip_file_path = template_card.temp_file.path
        zip_file_name = os.path.splitext(os.path.basename(zip_file_path))[0]

        # Create a directory to extract the contents of the zip file
        extracted_dir = os.path.join(settings.MEDIA_ROOT, "templates", zip_file_name)
        os.makedirs(extracted_dir, exist_ok=True)

        # Extract the contents of the zip file to the directory
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extracted_dir)

        # Get the path to the index.html file within the extracted directory
        index_html_path = os.path.join(extracted_dir, "index.html")

        # Read the content of the index.html file
        with open(index_html_path, 'r') as index_file:
            content = index_file.read()

        # Render the content within an HTML template
        return render(request, "frame.html", {"content": content})

    except TemplateCard.DoesNotExist:
        return HttpResponse("Template not found",status=404)
    





def premium_view(request, template_card_id):
    try:
        # Get the TemplateCard object by ID  
        template_card = PremiumCard.objects.get(id=template_card_id)

        # Extract necessary information from the TemplateCard
        zip_file_path = template_card.temp_file.path
        zip_file_name = os.path.splitext(os.path.basename(zip_file_path))[0]

        # Create a directory to extract the contents of the zip file
        extracted_dir = os.path.join(settings.MEDIA_ROOT, "templates", zip_file_name)
        os.makedirs(extracted_dir, exist_ok=True)

        # Extract the contents of the zip file to the directory
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extracted_dir)

        # Get the path to the index.html file within the extracted directory
        index_html_path = os.path.join(extracted_dir, "index.html")

        # Read the content of the index.html file
        with open(index_html_path, 'r') as index_file:
            content = index_file.read()

        # Render the content within an HTML template
        return render(request, "frame.html", {"content": content})

    except PremiumCard.DoesNotExist:
        return HttpResponse("Template not found",status=404)
    





def frame(request):
    return render(request,"frame.html")




def profile(request):
    return render(request,"profile.html")




def payment(request):
    return render(request,"payment.html")
def card(request):
    return render(request,"card.html")