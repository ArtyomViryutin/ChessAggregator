from django.db.models.signals import post_save
from django.dispatch import receiver
from djoser.serializers import UserSerializer


from .models import User
from .parse import parse

#
# @receiver(post_save, sender=User)
# def post_save_user(sender, instance, created, **kwargs):
#     if created:
#         ratings = parse(instance.frc_id, instance.fide_id)
#         serializer = UserSerializer(instance=instance, data=ratings, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
