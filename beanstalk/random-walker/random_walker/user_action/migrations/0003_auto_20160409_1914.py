# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-09 11:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_action', '0002_userprofile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(default='default.jpeg', upload_to='userprofile'),
        ),
    ]