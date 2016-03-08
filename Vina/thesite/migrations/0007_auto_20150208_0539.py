# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('thesite', '0006_auto_20150202_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='labelfile',
            field=models.FileField(upload_to=b'./data', blank=True),
            preserve_default=True,
        ),
    ]
