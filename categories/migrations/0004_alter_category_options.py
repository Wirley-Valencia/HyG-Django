# Generated by Django 4.2.7 on 2024-02-15 03:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0003_alter_category_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Categoria', 'verbose_name_plural': 'Categorias'},
        ),
    ]
