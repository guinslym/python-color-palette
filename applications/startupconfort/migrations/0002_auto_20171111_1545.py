# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-11 20:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('startupconfort', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gallery',
            name='num_vote_down',
        ),
        migrations.RemoveField(
            model_name='gallery',
            name='num_vote_up',
        ),
        migrations.RemoveField(
            model_name='gallery',
            name='vote_score',
        ),
    ]