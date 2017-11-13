# -*- coding: utf-8 -*-
from datetime import datetime

#Fixture package
from mixer.backend.django import mixer

#Test package & Utils
from django.test import TestCase
import pytest
pytestmark = pytest.mark.django_db

#models
from applications.wadiyabi.models import WadiyabiProduct
from applications.wadiyabi.models import BankAccount
from applications.wadiyabi.models import WadiyabiComment
from applications.wadiyabi.models import WadiyabiUserProfile
from applications.wadiyabi.models import WadiyabiLocation
from applications.wadiyabi.models import WadiyabiPurchase
from django.contrib.auth.models import User

#url helper
from django.core.urlresolvers import reverse, resolve

"""

___  ___          _      _
|  \/  |         | |    | |
| .  . | ___   __| | ___| |___
| |\/| |/ _ \ / _` |/ _ \ / __|
| |  | | (_) | (_| |  __/ \__ \
\_|  |_/\___/ \__,_|\___|_|___/

MVP model tests --- it's not extensive

"""
class TestWadiyabiProduct(TestCase):

    def tearDown(self):
        WadiyabiProduct.objects.all().delete()
        WadiyabiPurchase.objects.all().delete()

    def test_init(self):
        obj = mixer.blend('wadiyabi.WadiyabiProduct')
        assert obj.pk == 1, 'Should save an instance'

    def test_right_instance(self):
        obj = mixer.blend('wadiyabi.WadiyabiProduct')
        assert isinstance(obj, WadiyabiProduct) , 'Should be a WadiyabiProduct instance'

    def test_count_object(self):
        obj = mixer.cycle(10).blend('wadiyabi.WadiyabiProduct')
        assert WadiyabiProduct.objects.all().count() == 10

    def test_attributes_of_models(self):
        obj = mixer.blend('wadiyabi.WadiyabiProduct')
        assert obj.owner
        assert obj.picture
        assert obj.id
        assert obj.shortdesc
        assert obj.slug
        assert obj.price >= 0
        # ...

    def test_relation_has_a_user(self):
        user = mixer.blend(User, username='nickelback')
        obj = mixer.blend('wadiyabi.WadiyabiProduct', owner=user)
        self.assertTrue(obj.owner.username, 'nickelback')

    def test_relationship_one_to_many(self):
        """slow test

        Clue:
           WadiyabiProduct.objects.all().prefetch_related('user')
        """
        User.objects.all().delete()
        WadiyabiProduct.objects.all().delete()
        user = mixer.blend(User, username='nickelback')
        obj = mixer.cycle(5).blend('wadiyabi.WadiyabiProduct', owner=user)
        products = WadiyabiProduct.objects.all()
        for i in products:
            self.assertTrue(i.owner.username, 'nickleback')

class TestWadiyabiUserProfile(TestCase):
    def test_init(self):
        obj = mixer.blend('wadiyabi.WadiyabiUserProfile')
        assert obj.pk == 1, 'Should save an instance'

    def test_right_instance(self):
        obj = mixer.blend('wadiyabi.WadiyabiUserProfile')
        assert isinstance(obj, WadiyabiUserProfile) , 'Should be a WadiyabiUserProfile instance'

    def test_count_object(self):
        obj = mixer.cycle(10).blend('wadiyabi.WadiyabiUserProfile')
        assert WadiyabiUserProfile.objects.all().count() == 10

    def test_attributes_of_models(self):
        obj = mixer.blend('wadiyabi.WadiyabiUserProfile')
        assert obj.user
        assert obj.nickname
        assert obj.city
        assert obj.firstname
        assert obj.lastname
        assert obj.country
        # ...

    def test_relation_has_a_user(self):
        user = mixer.blend(User, username='nickelback')
        obj = mixer.blend('wadiyabi.WadiyabiUserProfile', user=user)
        self.assertTrue(obj.user.username, 'nickelback')

"""

______     _       _   _                 _     _
| ___ \   | |     | | (_)               | |   (_)
| |_/ /___| | __ _| |_ _  ___  _ __  ___| |__  _ _ __  ___
|    // _ \ |/ _` | __| |/ _ \| '_ \/ __| '_ \| | '_ \/ __|
| |\ \  __/ | (_| | |_| | (_) | | | \__ \ | | | | |_) \__ \
\_| \_\___|_|\__,_|\__|_|\___/|_| |_|___/_| |_|_| .__/|___/
                                                | |
                                                |_|

"""


class TestRelationship(object):
    def test_an_user_can_LIKE_a_product(self):
        user = mixer.blend(User, username='nickelback')
        product = mixer.blend('wadiyabi.WadiyabiProduct', owner=user)
        product.votes.up(user.id)
        assert product.votes.count() == 1

    def test_an_user_can_REGISTER_to_a_product(self):
        user = mixer.blend(User, username='nickelback')
        product = mixer.blend('wadiyabi.WadiyabiProduct', owner=user)
        purchase = mixer.blend('wadiyabi.WadiyabiPurchase',
                         vendor=user, product=product)
        assert purchase.vendor.username == 'nickelback'

        users = mixer.cycle(10).blend(User, username=mixer.sequence(lambda c: "nickelback_%s" % c))

        #registrering 10 users into a product
        for this_user in users:
            purchase = mixer.blend('wadiyabi.WadiyabiPurchase',
                vendor=this_user, product=product)

        #how many Student this WadiyabiProduct contains
        assert  WadiyabiPurchase.objects.filter(product= product.id).count() == 11

    def test_user_can_FOLLOW_a_user(self):
        from friendship.models import Friend, Follow

        user1 = mixer.blend(User, username='nickelback1')
        user2 = mixer.blend(User, username='nickelback2')
        following = Follow.objects.add_follower(user2, user1)
        #import pdb; pdb.set_trace()

        #List of a user's followers
        assert user2 in Follow.objects.followers(user1)
        #List of who a user is following
        assert user1 in Follow.objects.following(user2)

    def test_a_product_can_have_many_comments(self):
        user = mixer.blend(User, username='nickelback')
        product = mixer.blend(WadiyabiProduct, student=user)
        comments = mixer.cycle(12).blend(WadiyabiComment, user=user,
            product=product, comment=mixer.sequence(lambda c: "test_%s" % c))
        assert WadiyabiComment.objects.filter(product=product).count() == 12
        #TODO a user can post up to 4 comment to a product
