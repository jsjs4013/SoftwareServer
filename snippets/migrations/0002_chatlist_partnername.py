# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-29 15:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatlist',
            name='partnerName',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]