# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('thesite', '0002_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(default='example@example.com', help_text=b'A valid email address, please.', max_length=75),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default='password', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='headImg',
            field=models.FileField(upload_to=b'./upload'),
            preserve_default=True,
        ),
    ]
