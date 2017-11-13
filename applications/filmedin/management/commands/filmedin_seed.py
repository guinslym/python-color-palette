"""
from django.core.management.base import BaseCommand, CommandError

#Fixture package
from mixer.backend.django import mixer

#Test package & Utils
from django.test import TestCase
import pytest

#models
from applications.wadiyabi.models import Product
from applications.wadiyabi.models import BankAccount
from applications.wadiyabi.models import Comment
from applications.wadiyabi.models import UserProfile
from applications.wadiyabi.models import Location
from applications.wadiyabi.models import Purchase
from django.contrib.auth.models import User

try:
    from secrets import choice
except:
    from random import choice

from random import randint

class Command(BaseCommand):
    from faker import Factory
    fake = Factory.create()
    from mixer.backend.django import mixer

    help = 'Seeding the database'

    def handle(self, *args, **options):
        Product.objects.all().delete()
        BankAccount.objects.all().delete()
        Comment.objects.all().delete()
        UserProfile.objects.all().delete()
        Location.objects.all().delete()
        Purchase.objects.all().delete()
        User.objects.all().delete()
        self.stdout.write(
            self.style.SUCCESS(
                'Successfully Delete the Models \n\tNumber of users in the db: {} '.format(User.objects.all().count())
                )
            )

        mixer.cycle(15).blend(User)
        #admin user
        user=User.objects.create_user('admin', password='(famille)')
        user.is_superuser=True
        user.save()

        users = User.objects.all()
        for user in users:
            products = mixer.cycle( randint(1,5) ).blend(Product, author=user)
            for product in products:
                mixer.cycle( randint(1,3) ).blend(Comment, product=product, user=user)
            mixer.blend(UserProfile, user=user)
            mixer.blend(Location, user=user)
            mixer.blend(BankAccount, user=user)

        self.stdout.write(
            self.style.SUCCESS(
                'Successfully Seeding Models \n\tNumber of users in the db: %s '  % len(users)
                )
            )
        self.stdout.write(
            self.style.SUCCESS(
                'Created a User < admin > with password < (famille) > for you to login.'
                )
            )
"""
