from django.db import models
from django.contrib.auth.models import User
from mixins import CreatedUpdatedMixin

PRIORITIES = (
    (1, 'Low'),
    (2, 'Medium'),
    (3, 'High')
)


class Tags(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, null=True)


class Folder(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, null=True)


class Task(CreatedUpdatedMixin):
    title = models.TextField()
    description = models.TextField()
    parent = models.ForeignKey("self", null=True)
    tags = models.ManyToManyField(Tags)
    folder = models.ForeignKey(Folder, null=True)
    is_done = models.BooleanField(default=False)
    due_date = models.DateTimeField(null=True)
    completed_date = models.DateTimeField(null=True)
    priority = models.IntegerField(choices=PRIORITIES, default=2)
    owner = models.ForeignKey(User, null=True)

class Notes(CreatedUpdatedMixin):
    task = models.ForeignKey(Task)
    notes = models.TextField()

