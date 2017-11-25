# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-11 03:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0002_add_send_events'),
    ]

    operations = [
        migrations.AddField(
            model_name='messagetemplate',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='messagetemplate',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='scheduledmessage',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='scheduledmessage',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]