# Generated by Django 5.0.6 on 2024-06-22 09:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('comments', '0001_initial'),
        ('entries', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='all_comments', to='entries.entry'),
        ),
    ]