# Generated by Django 4.2.7 on 2024-03-11 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_remove_product_cantidad_disponible_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='total_cantidad_disponible',
            field=models.IntegerField(default=0),
        ),
    ]
