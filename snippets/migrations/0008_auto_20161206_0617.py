# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-06 06:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0007_auto_20161206_0345'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usedbook',
            options={'ordering': ('sellerPrice',)},
        ),
    ]
