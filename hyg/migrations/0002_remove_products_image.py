# Generated by Django 4.2.7 on 2023-12-01 04:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hyg', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='image',
        ),
    ]
