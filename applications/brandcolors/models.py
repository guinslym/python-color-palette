from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, RegexValidator
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.urlresolvers import reverse_lazy, reverse
from django.core.exceptions import ValidationError
from stdimage.utils import pre_delete_delete_callback, pre_save_delete_callback
from django.utils.timezone import now
from stdimage.models import StdImageField

from django.db.models.signals  import post_delete, pre_save

#other package

#from utils.models_utils import TimeStampedModel

from autoslug import AutoSlugField
from autoslug.settings import slugify as default_slugify

# pip install dhcpkit
import codecs
import re
from typing import Iterable, Tuple, Union

from allauth.account.signals import user_signed_up, user_logged_in
from django.dispatch import receiver

from django.core.validators import MinValueValidator

class AutoCreatedField(models.DateTimeField):
    """
    A DateTimeField that automatically populates itself at
    object creation.
    By default, sets editable=False, default=datetime.now.
    """
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('editable', False)
        kwargs.setdefault('default', now)
        super(AutoCreatedField, self).__init__(*args, **kwargs)

class AutoLastModifiedField(AutoCreatedField):
    """
    A DateTimeField that updates itself on each save() of the model.
    By default, sets editable=False and default=datetime.now.
    """
    def pre_save(self, model_instance, add):
        value = now()
        setattr(model_instance, self.attname, value)
        return value

class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields.
    """
    created = AutoCreatedField(_('created'))
    modified = AutoLastModifiedField(_('modified'))

    class Meta:
        abstract = True


"""
___  ___          _      _
|  \/  |         | |    | |
| .  . | ___   __| | ___| |___
| |\/| |/ _ \ / _` |/ _ \ / __|
| |  | | (_) | (_| |  __/ \__ \
\_|  |_/\___/ \__,_|\___|_|___/

MVP model tests --- it's not extensive

"""

class Startup(TimeStampedModel, models.Model):
    title = models.CharField(verbose_name=_(u"Title"), max_length=50)
    slug = models.SlugField(blank=True, null=True)
    brand_url = models.URLField(blank=True, null=True)
    source_url = models.URLField(blank=True, null=True)


    def __str__(self):
        return "{}".format(self.title)

    def __repr__(self):
        return "\ntitle    : #{}\nslug      : {}\nbrand_url : {}\nsource_url: {}".format(
            self.title, self.slug, self.brand_url, self.source_url
            )

    class Meta:
        verbose_name_plural = "Startups"
        verbose_name = "Startup"

    def get_absolute_url(self):
        return reverse('Startup', kwargs={'pk':self.id})


class StartupColor(TimeStampedModel, models.Model):
    color =models.CharField(verbose_name=_(u"Color"), max_length=6)
    red = models.PositiveSmallIntegerField(blank=True, null=True)
    green = models.PositiveSmallIntegerField(blank=True, null=True)
    blue = models.PositiveSmallIntegerField(blank=True, null=True)
    startup = models.ForeignKey(
        Startup, null=False, blank=False
        , related_name='brand_color')
    def __str__(self):
        return "{}".format(self.color)

    def __repr__(self):
        return "\nColor  : #{0}\nStartup: {1}\nred : {2}\ngreen : {3}\nblue : {4}".format(self.color, self.startup.title, self.red, self.green, self.blue)


    class Meta:
        verbose_name_plural = "Colors"
        verbose_name = "Color"

    def get_absolute_url(self):
        return reverse('Color', kwargs={'pk':self.id})

class Fabric(TimeStampedModel):
    picture = StdImageField(upload_to='fabrics/%Y/%m/%d',
                            verbose_name="pics", blank=True, null=True, variations={
        'large': (600, 400),
        'thumbnail': (250, 250, True),
        'medium': (300, 200),
    })
    class Meta:
        ordering = ["-created"]
        #ordering = ("?",)
        verbose_name = 'Fabric'
        verbose_name_plural = 'Fabric'
