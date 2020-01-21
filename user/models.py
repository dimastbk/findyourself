from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

from index.models import City, Place


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, verbose_name='Краткая информация')
    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Населённый пункт',
        help_text='Используется для показа пути от этого места до начала маршрута.',
    )
    instagram = models.CharField(max_length=50, blank=True)
    like_place = models.ManyToManyField(
        Place,
        verbose_name='Избранное',
        db_table='like_user_place',
        related_name='like_place',
    )
    done_place = models.ManyToManyField(
        Place,
        verbose_name='Пройденные места',
        db_table='done_user_place',
        related_name='done_place',
    )
    want_place = models.ManyToManyField(
        Place,
        verbose_name='Планируемые места',
        db_table='want_user_place',
        related_name='want_place',
    )

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('user:profile', kwargs={'pk': self.id})


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
