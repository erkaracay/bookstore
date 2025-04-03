from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group
from django.dispatch import receiver

def create_user_groups():
    Group.objects.get_or_create(name='Buyer')
    Group.objects.get_or_create(name='Seller')
    Group.objects.get_or_create(name='Admin')

@receiver(post_migrate)
def create_groups(sender, **kwargs):
    create_user_groups()
