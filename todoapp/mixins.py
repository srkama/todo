__author__ = 'kamal.s'

from django.db import models
from django.contrib.auth.models import User


class CreatedUpdatedMixin(models.Model):
    """
    a Mixin to Capture Created and Updated by and Time
    """
    created_by = models.ForeignKey(User,
                                   related_name="%(app_label)s_%(class)s_adder",
                                   on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    modified_by = models.ForeignKey(User,
                                    related_name="%(app_label)s_%("
                                                 "class)s_editor",
                                    on_delete=models.PROTECT)
    modified_date = models.DateTimeField(auto_now=True,
                                         editable=False)

    class Meta:
        abstract = True