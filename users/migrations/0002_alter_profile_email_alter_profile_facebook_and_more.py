# Generated by Django 5.0.6 on 2024-06-25 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='email',
            field=models.EmailField(blank=True, default='@', max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='facebook',
            field=models.URLField(blank=True, default='#', null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='instagram',
            field=models.URLField(blank=True, default='#', null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='spotify',
            field=models.URLField(blank=True, default='#', null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='twitter',
            field=models.URLField(blank=True, default='#', null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='website',
            field=models.URLField(blank=True, default='#', null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='youtube',
            field=models.URLField(blank=True, default='#', null=True),
        ),
    ]