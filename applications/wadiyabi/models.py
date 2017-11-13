# -*- coding: utf-8 -*-

#Python standard library
import datetime
import json
import uuid

#Django package
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, RegexValidator
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from utils.models_utils import unique_slug_generator

#other package
from vote.models import VoteModel

from utils.models_utils import TimeStampedModel

from autoslug import AutoSlugField


from django.utils.text import slugify
import string
from autoslug.settings import slugify as default_slugify
from django.conf import settings

try:
    #python 3.6 cryptographic random
    from secrets import choice
except:
    from random import choice


def random_string_generator(
        size=10,
        chars=string.ascii_lowercase + string.digits):
    """
    return a random string
    """
    return ''.join(choice(chars) for _ in range(size))

def custom_slugify(value):
    """
    will return hello_world_my_dear_s4lkj
    """
    return default_slugify(
        value \
        + " " + \
        random_string_generator(size=14)).replace('-', '_'
        )
from django.db.models.signals import pre_save
from django.dispatch import receiver

"""
@receiver(pre_save, sender=Product)
def add_content_to_the_slugfield(sender, instance, *args, **kwargs):
    instance.slug = slugify(instance.title)
"""

class WadiyabiProduct(TimeStampedModel, VoteModel, models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=False, blank=False
        , related_name='vendor')
    picture = models.ImageField(upload_to='wadiyabi/%Y/%m/%d',
                            help_text='Show us wadiyabi',
                            null=False, blank=False, verbose_name="pics")
    shortdesc = models.CharField(max_length=80, null=False, blank=False, verbose_name='shoutout')
    slug  = AutoSlugField(
            slugify=custom_slugify,
            unique_with=('created', 'owner'),
                        )
    price = models.DecimalField(max_digits=16, decimal_places=2, default=0, null=True, blank=True)
    activated = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(10),])
    #did this product have been sale
    sale = models.BooleanField(default=False)


    def __str__(self):
        return str(self.idUser)

    def __repr__(self):
        return '\nid\t\t:{}\nprice\t\t:{}\nslug\t\t:{}\nshortdesc\t:{}\n'.format(
            self.id, self.price ,self.slug, self.shortdesc[:5]
            )

    def get_absolute_url(self):
        return reverse('wadiyabi:product_detail', args=(self.slug,))

    def get_owners(self):
        if self.owners:
            return '%s' % " / ".join([owner.username for owner in self.owners.all()])

    class Meta:
        ordering = ["-created"]
        #ordering = ("?",)
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class WadiyabiPurchase(TimeStampedModel, models.Model):
    product = models.ForeignKey(WadiyabiProduct)
    vendor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="purchase_vendor")
    client = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="purchase_client")

    class Meta:
        ordering = ["-created"]
        #ordering = ("?",)
        verbose_name = 'Purchase'
        verbose_name_plural = 'Purchases'

class WadiyabiComment(TimeStampedModel, VoteModel, models.Model):
    product = models.ForeignKey(WadiyabiProduct, on_delete=models.CASCADE, related_name='wadiyabi_commentaire')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wadiyabi_owner')
    comment = models.CharField(max_length=500)

    class Meta:
        ordering = ["-created"]
        #ordering = ("?",)
        verbose_name = 'Commnent'
        verbose_name_plural = 'Comments'

class WadiyabiUserProfile(TimeStampedModel, models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='wadiyabi_profile'
        )
    nickname = models.CharField(max_length=50, blank=False)
    firstname = models.CharField(max_length=50, blank=False)
    lastname = models.CharField(max_length=50, blank=False)
    country = models.CharField(max_length=50, blank=False)
    city = models.CharField(max_length=50, blank=False)
    bio = models.TextField()
    slug = models.SlugField()
    mobile = models.TextField(default='Your Mobile Phone Number')
    address = models.TextField(default='Your Address', null=False, blank=False)
    userpicture = models.ImageField(upload_to="my_profile/%Y/%m/%d", null=False, blank=False)

    def __str__(self):
        return str(self.slug)

    def __repr__(self):
        return '\nid\t\t:{}\nfullname\t:{}, {}\n'.format(
            self.id, self.firstname, self.lastname
            )

    @property
    def fullname(self):
        return (self.firstname + ", " + self.lastname)

    def get_absolute_url(self):
        return reverse('wadiyabi:userprofile_detail', args=(self.slug,))

    class Meta:
        ordering = ["-created"]
        #ordering = ("?",)
        verbose_name = 'UserProfile'
        verbose_name_plural = 'UserProfiles'

class WadiyabiLocation(TimeStampedModel, models.Model):
    user =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Location_gps')
    latitude = models.CharField(max_length=40)
    longitude = models.CharField(max_length=40)

    class Meta:
        ordering = ["-created"]
        #ordering = ("?",)
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'


class BankAccount(TimeStampedModel, models.Model):
    user =  models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wadiyabi_bank')
    balance = models.DecimalField(
                            max_digits=16,
                            decimal_places=2,
                            default=5)
    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return '\nid\t\t:{}\nbalance\t\t:$ {}\nusername\t:{}\n'.format(
            self.id, self.balance, self.user.username
            )

    def get_absolute_url(self):
        return reverse('wadiyabi:bank_account_detail', args=(self.id,))

    class Meta:
        ordering = ["-created"]
        #ordering = ("?",)
        verbose_name = 'BankAcount'
        verbose_name_plural = 'BankAccounts'
