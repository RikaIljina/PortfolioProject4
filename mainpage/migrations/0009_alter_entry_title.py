# Generated by Django 5.0.6 on 2024-06-03 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0008_delete_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
