# Generated by Django 4.1.2 on 2024-02-29 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0033_paymentsuccess_coupen_code_paymentsuccess_email_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentsuccess',
            name='coupen_code',
        ),
        migrations.RemoveField(
            model_name='paymentsuccess',
            name='email',
        ),
        migrations.RemoveField(
            model_name='paymentsuccess',
            name='final_amount',
        ),
        migrations.RemoveField(
            model_name='paymentsuccess',
            name='host_name',
        ),
        migrations.RemoveField(
            model_name='paymentsuccess',
            name='plan',
        ),
        migrations.RemoveField(
            model_name='paymentsuccess',
            name='razorpay_order_id',
        ),
        migrations.RemoveField(
            model_name='paymentsuccess',
            name='razorpay_payment',
        ),
        migrations.RemoveField(
            model_name='paymentsuccess',
            name='template_amount',
        ),
        migrations.RemoveField(
            model_name='paymentsuccess',
            name='template_category',
        ),
        migrations.RemoveField(
            model_name='paymentsuccess',
            name='template_img',
        ),
        migrations.RemoveField(
            model_name='paymentsuccess',
            name='template_name',
        ),
        migrations.RemoveField(
            model_name='paymentsuccess',
            name='username',
        ),
    ]
