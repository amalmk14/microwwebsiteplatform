import os
import zipfile
import razorpay
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils import timezone

from loginregister.models import Profile
from .models import *
from random import shuffle
# Create your views here.


def home(request):
    name = request.session.get('username')

    template_categories = Templates.objects.filter(temp_type__name='normal').values_list('category', flat=True).distinct()

    # Filter templates based on selected category or get all templates
    selected_category = request.GET.get('category')
    if selected_category:
        normal = Templates.objects.filter(temp_type__name='normal', category=selected_category)
    else:
        normal_type = TemplatesType.objects.get(name='normal')
        normal = Templates.objects.filter(temp_type=normal_type)

    # Shuffle the normal templates
    normal_list = list(normal)
    shuffle(normal_list)
    
    premium_type = TemplatesType.objects.get(name='premium')
    premiums = Templates.objects.all().filter(temp_type=premium_type)

    # Shuffle the normal templates
    premium_list = list(premiums)
    shuffle(premium_list)

    # Take the first 6 items
    random_premium = premium_list[:8]
    paginators = Paginator(random_premium, 8)

    # paginators = Paginator(premiums, 8)
    try:
        pages = int(request.GET.get('page', "1"))
    except:
        pages = 1
    try:
        premiums = paginators.page(pages)
    except (EmptyPage, InvalidPage):
        premiums = paginators.page(paginators.num_pages)

    # Check if the show_modal key is not present in the session
    show_modal = request.session.get('show_modal', True)
    # Set show_modal to False to prevent showing the modal on subsequent visits
    request.session['show_modal'] = False

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        Contact(name=name,email=email,subject=subject,message=message,date=timezone.now()).save()
        messages.info(request,"Message Sent Successfully")
        return redirect('mainapp:home')
    return render(request,'home.html',{'normal':normal_list,'premiums':premiums,'name':name,'show_modal': show_modal,'template_categories': template_categories,'selected_category': selected_category})


from django.http import JsonResponse
from django.urls import reverse
from .models import Templates, TemplatesType

def get_templates_by_category(request):
    selected_category = request.GET.get('category')
    
    if selected_category:
        templates = Templates.objects.filter(category=selected_category)[:6]
    else:
        templates = Templates.objects.all().order_by('?')[:6]

    template_data = []
    for template in templates:
        template_data.append({
            'id': template.id,
            'name': template.name,
            'img_url': template.temp_img.url,
            'preview_url': reverse('mainapp:temp_view', args=[template.id]),
        })

    return JsonResponse({'templates': template_data})



def temp_view(request, template_card_id):
    try:
        # Get the TemplateCard object by ID
        template_card = Templates.objects.get(id=template_card_id)

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
        return render(request, "frame.html", {"content": content,'template_card':template_card})

    except Templates.DoesNotExist:
        return HttpResponse("Template not found",status=404)


def morePremium(request):
    # Retrieve the template categories for the dropdown
    template_categories = Templates.objects.filter(temp_type__name='premium').values_list('category', flat=True).distinct()

    # Filter templates based on selected category or get all templates
    selected_category = request.GET.get('category')
    if selected_category:
        premium = Templates.objects.filter(temp_type__name='premium', category=selected_category)
    else:
        premium_type = TemplatesType.objects.get(name='premium')
        premium = Templates.objects.filter(temp_type=premium_type)

    # Shuffle the normal templates
    premium_list = list(premium)
    shuffle(premium_list)

    # Render the template with the context data
    return render(request, 'morepremium.html', {'premium': premium_list, 'template_categories': template_categories})


def moreNormal(request):
    # Retrieve the template categories for the dropdown
    template_categories = Templates.objects.filter(temp_type__name='normal').values_list('category', flat=True).distinct()

    # Filter templates based on selected category or get all templates
    selected_category = request.GET.get('category')
    if selected_category:
        normal = Templates.objects.filter(temp_type__name='normal', category=selected_category)
    else:
        normal_type = TemplatesType.objects.get(name='normal')
        normal = Templates.objects.filter(temp_type=normal_type)

    # Shuffle the normal templates
    normal_list = list(normal)
    shuffle(normal_list)

    # Render the template with the context data
    return render(request, 'morenormal.html', {'normal': normal_list, 'template_categories': template_categories})


# def contact_us(request):
#     if request.method == 'POST':
#         name = request.POST['name']
#         email = request.POST['email']
#         subject = request.POST['subject']
#         message = request.POST['message']
#         Contact(name=name,email=email,subject=subject,message=message,date=timezone.now())


def pay(request,template_id):
    temp_card =Templates.objects.get(id=template_id)
    return render(request,'pay/payment2.html',{'temp_card':temp_card})

def coupen(request,id):
    template_card = Templates.objects.get(id=id)
    if request.method == 'POST':
        code = request.POST['coupen_code']
        if Coupen_code.objects.filter(code=code).exists():
            coupens = Coupen_code.objects.get(code=code)
            amount = template_card.price
            percentage = coupens.coupen_percentage

            discounts = amount*(percentage/100)
            discount=round(discounts)

            final_price = amount-discount
            request.session['code'] = code
            request.session['percentage'] = percentage
            request.session['final_price'] = final_price

            percentage = request.session.get('percentage')
            final_price = request.session.get('final_price')

            context = {
                'discount':discount,
                'percentage':percentage,
                'temp_card':template_card,
                'final_price':final_price
            }
            return render(request,'pay/payment2.html',context)
        else:
            messages.info(request,'Invalid Code')
            return redirect('mainapp:pay',id)

def delcoupen(request,template_id):
    if 'code' in request.session:
        del request.session['code']
        del request.session['percentage']
        del request.session['final_price']
        request.session.save()
        return redirect('mainapp:pay',template_id)

# def checkout(request,id):
#     template = Templates.objects.get(id=id)
#     if request.method == 'POST':
#         host = request.POST['host']
#         name = request.session.get('username')
#         if name:
#             profile_object = Profile.objects.get(name=name)
#             email = profile_object.email
#
#             try:
#                 counter = 1
#                 while Orders.objects.filter(finder=f"{email} {counter}").exists():
#                     counter += 1
#
#                 finder = f"{email} {counter}"
#                 request.session['finder'] =finder
#                 request.session.save()
#             except Orders.DoesNotExist:
#                 print("no data")
#
#             if request.session.get('final_price',None):
#                 final_amount = request.session.get('final_price',None)
#             else:
#                 final_amount = int(template.price)
#
#
#             finder = request.session.get('finder',None)
#             code = request.session.get('coupen_code',None)
#             orders = Orders(username=name,email=email,template_name=template.name,template_amount=template.price,template_category=template.category,finder=finder,order_date=timezone.now(),final_amount=final_amount,coupen_code=code,host_name=host)
#             orders.save()
#     client = razorpay.Client(auth=(settings.KEY,settings.SECRET))
#     payment = client.order.create({'amount':template.price * 100,'currency':'INR','payment_capture':1})
#     finder = request.session.get('finder',None)
#     orders_obj = Orders.objects.get(finder=finder)
#     orders_obj.razorpay_order_id=payment['id']
#     orders_obj.save()
#     context = {
#         'payment': payment,
#         'name': name
#     }
#     return render(request,"pay/checkout.html",context)


from django.core.exceptions import ObjectDoesNotExist

# ...

def checkout(request, id):
    template = Templates.objects.get(id=id)

    if request.method == 'POST':
        host = request.POST['host']
        name = request.session.get('username')

        if name:
            profile_object = Profile.objects.get(name=name)
            email = profile_object.email

            if request.session.get('final_price', None):
                final_amount = request.session.get('final_price', None)
            else:
                final_amount = int(template.price)

            existing_order = Orders.objects.filter(email=email, amount_paid=False).first()
            code = request.session.get('coupen_code', None)

            if Orders.objects.filter(email=email, amount_paid=True).exists():
                messages.error(request, "You have already purchased a template.")
                return redirect('mainapp:home')

            elif existing_order:
                # Delete the existing order
                existing_order.delete()

            orders = Orders(username=name, email=email, template_name=template.name,template_img=template.temp_img,
                            template_id=template.id,template_amount=template.price, template_category=template.category,
                            order_date=timezone.now(), final_amount=final_amount, coupen_code=code,host_name=host)
            orders.save()

    client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
    payment = client.order.create({'amount': final_amount * 100, 'currency': 'INR', 'payment_capture': 1})

    try:
        orders_obj = Orders.objects.get(email=email)
        orders_obj.razorpay_order_id = payment['id']
        orders_obj.save()

        context = {
            'payment': payment,
            'name': name
        }

        return render(request, "pay/checkout.html", context)

    except ObjectDoesNotExist:
        # Handle the case where the order with the specified email does not exist
        messages.error(request, "Order not found.")
        return redirect('mainapp:home')  # Adjust the redirect URL as needed


# # def success(request):
# #     order_id = request.GET.get('Order_id')
# #     orders = Orders.objects.get(razorpay_order_id=order_id)
# #     orders.amount_paid=True
# #     orders.save()
# #     return render(request,'pay/paymentsuccess.html')

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

# Modify your views.py file
from datetime import timedelta
from django.shortcuts import get_object_or_404

def success(request):
    order_id = request.GET.get('Order_id')
    # orders = Orders.objects.get(razorpay_order_id=order_id)
    current_user = request.session.get('username')

    orders = Orders.objects.filter(username=current_user, razorpay_order_id=request.GET.get('Order_id')).first()

    # Check if the payment success record already exists
    payment_success = PaymentSuccess.objects.filter(order=orders).first()

    if not payment_success:
        # Create a new PaymentSuccess record for the order
        expiry_date = orders.order_date + timedelta(days=2)
        countdown = (expiry_date - timezone.now()).days
        payment_success = PaymentSuccess(order=orders, expiry_date=expiry_date, countdown=countdown, payment_status=True)
        payment_success.save()

        reminder_date = expiry_date - timedelta(days=1)
        renewal = Renewal(order=orders, payment_success=payment_success, expiry_date=expiry_date, reminder_date=reminder_date)
        renewal.save()

        # Check if a coupon code was used
        coupen_code_used = request.session.get('code', None)

        if coupen_code_used:
            # Delete the used coupon code
            coupen_code = get_object_or_404(Coupen_code, code=coupen_code_used)
            coupen_code.delete()
            # Clear the coupon session
            request.session.pop('code', None)

    # Update the order's amount_paid status
    orders.amount_paid = True
    orders.save()
    # Send email to user with order details
    send_order_confirmation_email(orders)
    return render(request, 'pay/paymentsuccess.html',{'order': orders,'payment_success': payment_success})



def send_order_confirmation_email(orders):
    subject = 'Order Confirmation'
    message = render_to_string('email/order_confirmation_email.txt', {'orders': orders})
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [orders.email]

    send_mail(subject, message, from_email, to_email, fail_silently=False)

    # You can also log or handle errors here if the email fails to send


def paymentfailed(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login & Try Again")
        return redirect('register:login')
    order_id = request.GET.get('Order_id')
    orders = Orders.objects.get(razorpay_order_id=order_id)
    orders.amountpaid = False
    orders.paymentstatus = "failed"
    print("faild")
    orders.save()

    orders_id = request.GET.get('Order_id')
    print(orders_id)
    reason = request.GET.get('reason')
    code = request.GET.get('code')
    source = request.GET.get('source')
    step = request.GET.get('step')
    payment_id = request.GET.get('payment_id')
    if PaymentFailed.objects.filter(order_id=orders_id).exists():

        print("failed alredy exists")
        return redirect('mainapp:somethingwentwrong')
    else:
        try:
            failed = PaymentFailed(order_id=orders_id, reason=reason, code=code, source=source, step=step,
                                   payment_id=payment_id, date_time=timezone.now())
            failed.save()
            time = timezone.now()
            uid = request.user.id
            uemail = request.user.email
            uname = request.user.first_name
            email_subject = "payment failed"
            message = render_to_string('pay/payment_failure_mail.html', {
                'orders_id': orders_id,
                'reason': reason,
                'code': code,
                'source': source,
                'step': step,
                'payment_id': payment_id,
                'uid': uid,
                'uname': uname,
                'uemail': uemail,
                'date': time

            })
            print("mail attemptting")
            email_from = settings.EMAIL_HOST_USER
            recipient_list = ['amalmk2k18@gmail.com']

            email_message = EmailMessage(email_subject, message, email_from, recipient_list)
            print(email_message)
            email_message.content_subtype = "html"
            email_message.send()

        except  Exception as e:
            print("something went wrong")
            print(f"Error sending email: {e}")
            return redirect('mainapp:somethingwentwrong')
    return render(request, "pay/paymentfailed.html", {'order_id':order_id})


def somethingwentwrong(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Login & Try Again")
        return redirect('register:login')
    return render(request,"pay/somethingwentwrong.html")

