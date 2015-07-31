__author__ = 'kamal.s'

from .models import Task, Notes
from django.db.models.signals import post_save, m2m_changed
from .tasks import update_index


def update_search_index(sender, **kwargs):
    instance = kwargs['instance']
    task = None
    if isinstance(instance,Notes):
        task = instance.task
    else:
        task = instance
    if task.parent:
        task = task.parent
    update_index(task)


post_save.connect(update_search_index,sender=Task)
m2m_changed.connect(update_search_index,sender=Task.tags.through)
post_save.connect(update_search_index,sender=Notes)

