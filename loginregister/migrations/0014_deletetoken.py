# Generated by Django 4.1.2 on 2024-02-27 16:08

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('loginregister', '0013_profile_delete_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeleteToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='loginregister.profile')),
            ],
        ),
    ]
