# Generated by Django 5.0.6 on 2024-06-09 12:49

import cloudinary.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('users', '0001_initial'), ('users', '0002_alter_profile_bio'), ('users', '0003_alter_profile_bio')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, null=True)),
                ('pic', cloudinary.models.CloudinaryField(default='placeholder', max_length=255, verbose_name='image')),
                ('joined', models.DateTimeField(auto_now_add=True)),
                ('social', models.URLField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
