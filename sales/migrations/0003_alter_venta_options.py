# Generated by Django 4.2.7 on 2024-03-16 20:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0002_alter_venta_total'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='venta',
            options={'verbose_name': 'Venta', 'verbose_name_plural': 'Ventas'},
        ),
    ]
