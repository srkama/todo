__author__ = 'kamal.s'

from rest_framework.decorators import list_route, detail_route
from rest_framework.reverse import reverse_lazy, reverse
from rest_framework import serializers

from .models import Tags, Task, Notes, User, Folder


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer of USer model
    """
    tasks_url = serializers.SerializerMethodField(
        method_name='get_profile_tasks_url')

    class Meta:
        model = User
        exclude = ('password','is_superuser','is_staff','is_active',
                   'date_joined','email', 'user_permissions', 'groups')

    def get_profile_tasks_url(self, obj):
        """
        Method for task different end points for folders
        :param obj: user boj
        :return: dict of url end points
        """
        urls = {'inbox': reverse('task-list')}
        for folder in obj.folder_set.all():
            urls.update({
                folder.name:reverse('task-list')+'?f='+str(folder.id)})
        return urls


class MinimumUserSerializer(serializers.ModelSerializer):
    """
    Minimal Serializer version for User Model
    """
    class Meta:
        model = User
        exclude = ('password','is_superuser','is_staff','is_active',
                   'date_joined','email', 'user_permissions', 'groups')


class TagsSerializer(serializers.ModelSerializer):
    """
    Serializer for Tag
    """
    class Meta:
        model = Tags
        exclude = ('user',)


class FolderSerializer(serializers.ModelSerializer):
    """
    Serializer for Folder
    """
    class Meta:
        model = Folder
        exclude = ('user',)


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for Task Model
    """

    owner = MinimumUserSerializer(allow_null=True, read_only=True)
    tags = TagsSerializer(allow_null=True, many=True, read_only=True)
    task_uri = serializers.SerializerMethodField('get_task_urls')

    class Meta:
        model = Task
        exclude = ('folder', 'created_by', 'modified_by','parent')

    def get_task_urls(self, obj):
        """
        retuns end point for different operations tasks.
        :param obj: task obj
        :return: dict with url points
        """
        print obj
        kwargs={'pk': obj.id}
        url_names = ['task-manage-note',
                     'task-move-to-folder',
                     'task-manage-tags',
                     'task-notes',
                     'task-toggle-done']
        urls = {}
        for url_name in url_names:
            urls[url_name.replace('task-', '')]=reverse_lazy(url_name, [obj.id])
        if obj.task_set.count():
            urls['sub-tasks']=reverse_lazy('task-sub-tasks', [obj.id])
        return urls


class NotesSerializer(serializers.ModelSerializer):
    """
    Serializer for Notes Model
    """
    created_by = MinimumUserSerializer(allow_null=True, read_only=True)
    modified_by = MinimumUserSerializer(allow_null=True, read_only=True)
    class Meta:
        model = Notes
        exclude = ('task',)

