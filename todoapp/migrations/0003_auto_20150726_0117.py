# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0002_auto_20150726_0100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='folder',
            field=models.ForeignKey(to='todoapp.Folder', null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='is_done',
            field=models.BooleanField(default=False),
        ),
    ]
