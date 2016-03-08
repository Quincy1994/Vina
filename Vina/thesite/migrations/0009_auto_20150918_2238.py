# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('thesite', '0008_auto_20150321_1438'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='id',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='file',
            field=models.FileField(upload_to=b'./data/'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='labelfile',
            field=models.FileField(upload_to=b'./data/', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
