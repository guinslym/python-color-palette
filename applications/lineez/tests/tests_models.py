# -*- coding: utf-8 -*-
from datetime import datetime

#Fixture package
from mixer.backend.django import mixer

#Test package & Utils
from django.test import TestCase
import pytest
pytestmark = pytest.mark.django_db

#models
from applications.lineez.models import LineUpPost
from applications.lineez.models import Acceptance
from applications.lineez.models import LineezLocation
from django.contrib.auth.models import User


from django.db import models

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
class TestLineUpPost(TestCase):

    def tearDown(self):
        LineUpPost.objects.all().delete()

    def test_init(self):
        obj = mixer.blend('lineez.LineUpPost')
        assert obj.pk == 1, 'Should save an instance'

    def test_right_instance(self):
        obj = mixer.blend('lineez.LineUpPost')
        assert isinstance(obj, LineUpPost) , 'Should be a LineUpPost instance'

    def test_count_object(self):
        obj = mixer.cycle(10).blend('lineez.LineUpPost')
        assert LineUpPost.objects.all().count() == 10

    def test_attributes_of_models(self):
        obj = mixer.blend('lineez.LineUpPost')
        assert obj.title
        assert obj.description
        assert obj.id
        assert obj.time_host_wants_to_be_there
        assert obj.time_guest_must_be_there
        assert obj.owner
        # ...


    def test_relation_has_a_user(self):
        user = mixer.blend(User, username='nickelback')
        obj = mixer.blend('lineez.LineUpPost', owner=user)
        self.assertTrue(obj.owner.username, 'nickelback')

    def test_relationship_one_to_many(self):
        """slow test

        Clue:
           LineUpPost.objects.all().prefetch_related('user')
        """
        User.objects.all().delete()
        LineUpPost.objects.all().delete()
        user = mixer.blend(User, username='nickelback')
        obj = mixer.cycle(5).blend('lineez.LineUpPost', owner=user)
        products = LineUpPost.objects.all()
        for i in products:
            self.assertTrue(i.owner.username, 'nickleback')

    def test_relationship_acceptance(self):
        """slow test

        Clue:
           LineUpPost.objects.all().prefetch_related('user')
        """
        User.objects.all().delete()
        LineUpPost.objects.all().delete()
        user = mixer.blend(User, username='nickelback')
        user2 = mixer.blend(User)
        obj = mixer.cycle(5).blend('lineez.LineUpPost', owner=user)
        acceptance = mixer.blend(Acceptance, owner=user2, liner=user, lineup=obj[0])
        assert user is not user2
        acceptance.owner is not acceptance.liner

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
