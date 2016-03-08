# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('thesite', '0003_auto_20150129_1902'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BlogPost',
        ),
    ]
