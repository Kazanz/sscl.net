# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-09-03 21:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0012_receivedtext'),
    ]

    operations = [
        migrations.AddField(
            model_name='waiver',
            name='last_interaction',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]