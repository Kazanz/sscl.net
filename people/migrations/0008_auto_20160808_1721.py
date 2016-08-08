# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-08-08 17:21
from __future__ import unicode_literals

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0007_auto_20160808_1709'),
    ]

    operations = [
        migrations.RenameField(
            model_name='messagetracker',
            old_name='errors',
            new_name='email_errors',
        ),
        migrations.RenameField(
            model_name='messagetracker',
            old_name='success',
            new_name='email_success',
        ),
        migrations.AddField(
            model_name='messagetracker',
            name='txt_errors',
            field=jsonfield.fields.JSONField(default=[]),
        ),
        migrations.AddField(
            model_name='messagetracker',
            name='txt_success',
            field=jsonfield.fields.JSONField(default=[]),
        ),
    ]