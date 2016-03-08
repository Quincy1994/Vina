# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('thesite', '0005_auto_20150130_1537'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='user',
        ),
        migrations.DeleteModel(
            name='File',
        ),
        migrations.AddField(
            model_name='user',
            name='file',
            field=models.FileField(default='a flie', upload_to=b'./data'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='labelfile',
            field=models.FileField(default='a label file', upload_to=b'./data/label'),
            preserve_default=False,
        ),
    ]
