# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField()),
                ('created_by', models.ForeignKey(related_name='todoapp_notes_adder', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(related_name='todoapp_notes_editor', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('is_done', models.BooleanField()),
                ('due_date', models.DateTimeField()),
                ('completed_date', models.DateTimeField()),
                ('created_by', models.ForeignKey(related_name='todoapp_task_adder', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('folder', models.ForeignKey(to='todoapp.Folder')),
                ('modified_by', models.ForeignKey(related_name='todoapp_task_editor', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(to='todoapp.Task')),
                ('tags', models.ManyToManyField(to='todoapp.Tags')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='reminder',
            name='task',
            field=models.ForeignKey(to='todoapp.Task'),
        ),
        migrations.AddField(
            model_name='notes',
            name='task',
            field=models.ForeignKey(to='todoapp.Task'),
        ),
    ]
