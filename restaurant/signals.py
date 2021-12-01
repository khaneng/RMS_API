from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
# 	if created:
# 		is_subadmin = getattr(instance, 'is_subadmin', None)
# 		print("############",is_subadmin)
# 		print(instance.__dict__)
# 		Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
# 	print(instance.__dict__)
# 	instance.profile.save()
