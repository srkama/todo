__author__ = 'kamal.s'

from django.db import connection


def update_index(task):
    task_doc = [task.title, task.description]
    task_doc.extend(task.tags.all().values_list('name', flat=True))
    task_doc.extend(task.notes_set.all().values_list('notes', flat=True))
    task_doc.extend(task.task_set.all().values_list('title', flat=True))
    task_doc.extend(task.task_set.all().values_list('description', flat=True))
    cursor = connection.cursor()
    sql = """UPDATE todoapp_task
                        SET search_index = to_tsvector('english', COALESCE(%s,
                        ''))
                    WHERE id=%s"""
    cursor.execute(sql, [' '.join(task_doc), task.id])


