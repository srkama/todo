# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0005_auto_20150726_0136'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='priority',
            field=models.IntegerField(default=2, choices=[(1, b'Low'), (2, b'Medium'), (3, b'High')]),
        ),
    ]
