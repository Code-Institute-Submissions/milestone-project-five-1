# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-03-25 01:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0003_auto_20190325_0154'),
        ('accounts', '0002_auto_20190325_0148'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
