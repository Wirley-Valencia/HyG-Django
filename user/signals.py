from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import CustomUser


@receiver(post_save, sender=CustomUser)
def add_user_to_clients_group(sender, instance, created, **kwargs):
    if created:
        try:
            group1 = Group.objects.get(name='clientes')
        except Group.DoesNotExist:
            group1 = Group.objects.create(name='Administradores')
            group2 = Group.objects.create(name='Empleados')
            group3 = Group.objects.create(name='clientes')
        instance.groups.add(group1)
