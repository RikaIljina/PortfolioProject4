# Generated by Django 5.0.6 on 2024-06-01 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0006_alter_entry_audio_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='likes',
            field=models.IntegerField(default=0, null=True),
        ),
    ]