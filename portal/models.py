from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    ROLE_CHOICES = (
        ("PASSENGER", "Passenger"),
        ("DRIVER", "Driver")
    )
    phone_number = models.CharField(max_length=10, blank=False)
    id_number = models.CharField(max_length=8, blank=False)
    role = models.CharField(max_length=9, choices=ROLE_CHOICES, default="PASSENGER")
    is_profile = models.BooleanField(default=False)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
