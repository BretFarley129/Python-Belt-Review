# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-24 04:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('belt', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='content',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
