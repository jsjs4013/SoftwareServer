# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-30 07:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0004_auto_20161129_1632'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatlist',
            name='studentName',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
