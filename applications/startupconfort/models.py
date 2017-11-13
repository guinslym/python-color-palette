from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import User
from model_utils.models import TimeStampedModel
from django.core.validators import MinLengthValidator, RegexValidator
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.urlresolvers import reverse_lazy, reverse
from django.core.exceptions import ValidationError
from stdimage.utils import pre_delete_delete_callback, pre_save_delete_callback

from django.db.models.signals  import post_delete, pre_save

#other package
from vote.models import VoteModel

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



"""
___  ___          _      _
|  \/  |         | |    | |
| .  . | ___   __| | ___| |___
| |\/| |/ _ \ / _` |/ _ \ / __|
| |  | | (_) | (_| |  __/ \__ \
\_|  |_/\___/ \__,_|\___|_|___/

MVP model tests --- it's not extensive

"""


class Purchase(TimeStampedModel):
    owner = models.ForeignKey(
                settings.AUTH_USER_MODEL,
                related_name='customer')
    table = models.TextField()
    confirmation_number = models.CharField(max_length=10)

    class Meta:
        ordering = ["-created"]
        #ordering = ("?",)
        verbose_name = 'Purchase'
        verbose_name_plural = 'Purchased'



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

class Category(TimeStampedModel):
    title = models.CharField(verbose_name=_(u"Title"), max_length=32)
    slug  = AutoSlugField(unique_with=('title'))

    class Meta:
        verbose_name_plural = "Categories"
        verbose_name = "Category"


class StartupProduct(TimeStampedModel, VoteModel):
    startup = models.ForeignKey(
        Startup, null=False, blank=False
        , related_name='brand_product')
    category = models.ForeignKey(
        Category, null=False, blank=False
        , related_name='product_category')
    title = models.CharField(verbose_name=_(u"Title"), max_length=32)
    shortdesc = models.CharField(max_length=80, null=False, blank=False, verbose_name='shortdesc')
    slug  = AutoSlugField(
            unique_with=('created', 'startup'),
                        )
    price = models.IntegerField(default=28)
    quantity = models.PositiveIntegerField(verbose_name=_(u"Qty"), default=1, validators=[MaxValueValidator(10),MinValueValidator(1),])


    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return '\nid\t\t:{}\nprice\t\t:{}\nslug\t\t:{}\nshortdesc\t:{}\ncategory\t:{}\n'.format(
            self.id, self.price ,self.slug, self.shortdesc[:5], self.category.title
            )

    def get_absolute_url(self):
        return reverse('startupconfort:product_detail', args=(self.slug,))

    class Meta:
        ordering = ["-created"]
        #ordering = ("?",)
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

from settings.base import BASE_DIR
import random



from stdimage.models import StdImageField

class StartupProductImage(TimeStampedModel, VoteModel):
    shortdesc = models.CharField(max_length=80, null=True, blank=True, verbose_name='shortdesc')
    # product = models.OneToOneField(StartupProduct,
    #                             related_name='image',
    #                             on_delete=models.CASCADE,
    #                             primary_key=True,
    #                             )
    # picture = StdImageField(upload_to='startup-product/%Y/%m/%d',
    #                         verbose_name="pics", blank=True, variations={
    #     'large': (600, 400),
    #     'thumbnail': (250, 250, True),
    #     'medium': (300, 200),
    # })
    # color = models.ForeignKey(StartupColor, null=False, blank=False,
    #                             related_name='startup_color')
    #
    # def get_random_image(self):
    #     images = ['image250', 'tpillow250', 'tie250' ]
    #     random.shuffle(images)
    #     image = images[0] +'.jpg'
    #     return image
    #
    # def image_url(self):
    #     """
    #     Returns the URL of the image associated with this Object.
    #     If an image hasn't been uploaded yet, it returns a stock image
    #
    #     :returns: str -- the image url
    #
    #     """
    #     if self.image and hasattr(self.image, 'url'):
    #         return self.image.url
    #     else:
    #         return self.get_random_image

    class Meta:
        ordering = ["-created"]
        #ordering = ("?",)
        verbose_name = 'StartupProductImage'
        verbose_name_plural = 'StartupProductImages'


class Gallery(TimeStampedModel):
    product = models.OneToOneField(StartupProduct,
                                related_name='image',
                                on_delete=models.CASCADE,
                                primary_key=True,
                                )
    picture = StdImageField(upload_to='startup-product/%Y/%m/%d',
                            verbose_name="pics", blank=True, null=True, variations={
        'large': (600, 400),
        'thumbnail': (250, 250, True),
        'medium': (300, 200),
    })
    class Meta:
        ordering = ["-created"]
        #ordering = ("?",)
        verbose_name = 'Gallery'
        verbose_name_plural = 'Galleries'



post_delete.connect(pre_delete_delete_callback, sender=StartupProductImage)
pre_save.connect(pre_save_delete_callback, sender=StartupProductImage)






class StartupShopppingCart(TimeStampedModel):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=False, blank=False
        , related_name='buyer')
    product = models.ForeignKey(StartupProduct, null=False, blank=False,
                                related_name='shopping_cart_product')
    color = models.ForeignKey(StartupColor, null=False, blank=False,
                                related_name='shopping_cart_color')
    quantity = models.PositiveIntegerField(verbose_name=_(u"Qty"), default=1, validators=[MaxValueValidator(10),MinValueValidator(1),])
    startup = models.ForeignKey(StartupProduct, null=False, blank=False,
                                related_name='shopping_cart_startup')
    total_amount = models.PositiveIntegerField(blank=True, null=True)
    shipping_address = models.CharField(max_length=120, blank=True, null=True)
    customer_name = models.CharField(max_length=40, blank=True, null=True)
    cart_slug = AutoSlugField(
            unique_with=('created', 'product', 'color'),
                        )
    delivered = models.BooleanField(default=False)
    payment_success = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Shopping Cart'


from django.db.models.signals import post_save
from django.dispatch import receiver
# from rest_framework.authtoken.models import Token
from django.conf import settings

# This code is triggered whenever a new user has been created and saved to the database

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)


def is_email(username_or_email):
    '''
    Takes a string as a parameter, and checks
    if is valid email or username.
    :param username_or_email:
    :return:
    '''

    return bool("@" in username_or_email)


def get_user(username_or_email):
    '''
    Takes username or email as a parameter
    and returns user object
    :param self, username_or_email:
    :return User Object:
    '''

    queryset = User.objects
    try:
        return queryset.get(customer__email=username_or_email) if is_email(username_or_email) \
            else queryset.get(username=username_or_email)
    except Exception:
        return False


def get_customer(user):
    try:
        return user.customer
    except Exception:
        return False

# Create your models here.
class CartItem(TimeStampedModel, models.Model):
    customer = models.ForeignKey(User)
    product = models.ForeignKey(StartupProduct)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1)
    slug  = AutoSlugField(
            unique_with=('created', 'product', 'customer'),
                        )
    def get_absolute_url(self):
        return reverse('startupconfort:homepage', )

    def __str__(self):
        return "\nAdded to the cart:\n\tProduct:\t{0}_{3}\n\tQuantity:\t({1})\n\tCustomer:\t{2}\n\tSlug:\t\t{4}\n".format(
        self.product.title,
        self.quantity,
        self.customer,
        self.product.slug,
        self.slug
        )


class ShippingAddress(TimeStampedModel):

    COUNTRIES_CHOICES = (
    ('CAN', "Canada"),
    ('USA', "USA"),
    )
    # ('Europe', 'Europe'),

    country = models.CharField(max_length=9,choices=COUNTRIES_CHOICES,default="USA")
    customer = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='shipping_address',
        on_delete=models.CASCADE,
        primary_key=True,
        )
    total_amount = models.PositiveIntegerField(blank=True, null=True)
    customer_name = models.CharField(max_length=120)
    shipping_address = models.CharField(max_length=120)
    city = models.CharField(max_length=40)
    postal_code = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    telephone = models.CharField(max_length=15,  blank=True, null=True)
    billing_email = models.EmailField(max_length=80)
    cart_slug = AutoSlugField(
            unique_with=('created', 'customer'),
            editable=True,
                        )
    delivered = models.BooleanField(default=False)
    payment_success = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Shipping Address'
