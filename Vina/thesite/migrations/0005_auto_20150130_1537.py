# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('thesite', '0004_delete_blogpost'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datafile', models.FileField(upload_to=b'./data')),
                ('labalfile', models.FileField(upload_to=b'./data')),
                ('user', models.ForeignKey(to='thesite.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='user',
            name='headImg',
        ),
    ]
