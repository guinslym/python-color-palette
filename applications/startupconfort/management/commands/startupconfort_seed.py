from django.core.management.base import BaseCommand, CommandError

#Fixture package
from mixer.backend.django import mixer

#Test package & Utils
from django.test import TestCase
import pytest

import time, random

#models
from applications.startupconfort.models import Startup
from applications.startupconfort.models import StartupColor
from mixer.backend.django import mixer
mixer.cycle(100).blend(StartupColor)
mixer.cycle(100).blend(Startup)

from applications.startupconfort.models import Category
from applications.startupconfort.models import StartupProduct
from applications.startupconfort.models import Gallery as StartupProductImage
from django.contrib.auth.models import User

try:
    from secrets import choice
except:
    from random import choice

from random import randint
import json
from pprint import pprint

from webcolors import hex_to_rgb


def find_image(category):
    if category == 'pillow':
        return 0
    elif category == 'tie':
        return 0
    else:
        return 0

class Command(BaseCommand):
    from faker import Factory
    fake = Factory.create()
    from mixer.backend.django import mixer

    help = 'Seeding the database'

    def handle(self, *args, **options):
        start = time.clock()
        Startup.objects.all().delete()
        Category.objects.all().delete()
        StartupColor.objects.all().delete()
        StartupProduct.objects.all().delete()
        StartupProductImage.objects.all().delete()
        self.stdout.write(
            self.style.SUCCESS(
                'Successfully Delete the Models \n\tNumber of users in the db: {} '.format(User.objects.all().count())
                )
            )

        try:
            #admin user
            user=User.objects.create_user('admin', password='(famille)')
            user.is_superuser=True
            user.save()

            # create 15 users
            mixer.cycle(15).blend(User)
        except:
            pass

        users = User.objects.all()

        with open('fixtures/brandcolors.json') as data_file:
            data = json.load(data_file)

        #import pdb; pdb.set_trace()

        for brand in data:
            #startup
            source_url = data.get(brand).get('source_url')
            # import pytest; pytest.set_trace()
            Startup.objects.create(
                title = str(data.get(brand).get('title')),
                slug = data.get(brand).get('slug'),
                source_url = data.get(brand).get('source_url'),
                brand_url = data.get(brand).get('brand_url')
            )
            brand_name = Startup.objects.last()

            from pprint import pprint
            pprint(data.get(brand).get('title'))
            colors = data.get(brand).get('colors')
            for color in colors:
                r,g,b  = hex_to_rgb('#'+color)
                StartupColor.objects.create(color=color, startup=brand_name, red=r, green=g, blue=b)

        # shuffling
        startups = Startup.objects.order_by('?')
        colors = StartupColor.objects.order_by('?')

        pillow = Category.objects.create(title='Pillow')
        cover = Category.objects.create(title='Travel Pillow')
        tie = Category.objects.create(title='Tie')

        # Create 3 Products
        startups = startups[:20]
        for startup_name in startups:
            category = Category.objects.order_by('?').all()
            category = category.first()
            new_product = mixer.blend(StartupProduct, title='Pillow', startup=startup_name, category=category)
            # create 2 image associate with the products
            mixer.blend(
                StartupProductImage,
                product=new_product,
                color=colors[0]
            )


        # Changing the image picture
        import os
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        from django.core.files import File
        # picture = StartupProductImage.objects.last()
        # picture.picture.save('apc.png', File(open(BASE_DIR+'/image250.jpg', 'rb')))
        #
        # pictures = StartupProductImage.objects.all()
        # for pic in pictures:
        #     pic.picture = StartupProductImage.objects.last().picture
        #     pic.save()

        from random import shuffle
        startups = ['Facebook', 'Twitter', 'Amazon', 'NBA', 'NFL']
        products = StartupProduct.objects.all()
        for product in products:
            shuffle(startups)
            product.title = product.title + ' ' + startups[0]
            product.save()

        self.stdout.write(
            self.style.SUCCESS(
                'Successfully Seeding Models \n\tNumber of users in the db: %s '  % len(users)
                )
            )

        # Time elapse
        end = time.clock()
        hours = end//3600
        end = end - 3600*hours
        minutes = end//60
        seconds = end - 60*minutes

        self.stdout.write(
            self.style.SUCCESS(
                'Created a User < admin > with password < (famille) > for you to login.'
                )
            )

        # Time elapse
        self.stdout.write(
            self.style.SUCCESS(
                '\n\nTime elapse: %d:%d:%d' %(hours,minutes,seconds)
                )
            )

'''
from applications.startupconfort.models import Gallery as StartupProductImage
pic  = StartupProductImage.objects.last().picture
images =  StartupProductImage.objects.all()
for i in images:
    i.picture = pic
    i.save()

from random import shuffle
startups = ['Facebook', 'Twitter', 'Amazon', 'NBA', 'NFL']
products = StartupProduct.objects.all()
for product in products:
    shuffle(startups)
    product.title = product.title + ' ' + startups[0]
    product.save()
'''
