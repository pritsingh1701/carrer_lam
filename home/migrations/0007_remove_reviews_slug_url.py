# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-16 13:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20170916_1314'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviews',
            name='slug_url',
        ),
    ]