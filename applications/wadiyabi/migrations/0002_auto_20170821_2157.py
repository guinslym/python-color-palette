# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-22 01:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wadiyabi', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Comment',
            new_name='WadiyabiComment',
        ),
        migrations.RenameModel(
            old_name='UserProfile',
            new_name='WadiyabiUserProfile',
        ),
    ]
