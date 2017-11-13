from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import User
from model_utils.models import TimeStampedModel
from django.core.urlresolvers import reverse_lazy, reverse

#from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.db.models.signals import post_save

class LineUpPost(TimeStampedModel):
    title = models.CharField(verbose_name=_(u"Title"), max_length=32)
    description = models.CharField(verbose_name=_(u"Description"), max_length=32)
    time_host_will_be_there = models.DateTimeField(verbose_name=_(u"time_host_will_be_there"))
    time_host_wants_to_be_there = models.DateTimeField(verbose_name=_(u"time_host_wants_to_be_there"))
    time_guest_must_be_there = models.DateTimeField(verbose_name=_(u"time_guest_must_be_there"))
    owner = models.ForeignKey(User)
    address = models.CharField(verbose_name=_(u"Address"), max_length=150)
    price = models.PositiveIntegerField(default=10)
    min_garanty_for_guest = models.PositiveIntegerField()
    min_garanty_for_host = models.PositiveIntegerField()
    latitude = models.CharField(verbose_name=_(u"Latitude"), max_length=32)
    longitude = models.CharField(verbose_name=_(u"Longitude"), max_length=32)

    def __str__(self):
        return "{}".format(self.title)
    class Meta:
        verbose_name_plural = "LineupPosts"
        verbose_name = "LineupPost"

    def get_absolute_url(self):
        return reverse('LineupPost', kwargs={'pk':self.id})

class Acceptance(TimeStampedModel):
    owner = models.ForeignKey(User, related_name='requester')
    liner = models.ForeignKey(User, related_name='stander')
    lineup = models.ForeignKey(LineUpPost, related_name='lineup')

    class Meta:
        verbose_name = 'Acceptance'
        verbose_name_plural = 'Acceptances'


class LineezLocation(TimeStampedModel, models.Model):
    user =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Lineez_gps')
    latitude = models.CharField(max_length=40)
    longitude = models.CharField(max_length=40)

    class Meta:
        ordering = ["-created"]
        #ordering = ("?",)
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'

#https://github.com/sseaver/TheIronBank/blob/efb90776cd272e46f6d440cdcf348b45a98c9452/app/models.py

"""
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
"""
