__author__ = 'kamal.s'

"""
Here we have defined all api END points to access tasks, user profile.
"""



from rest_framework.decorators import list_route, detail_route, api_view, \
    authentication_classes, permission_classes
from rest_framework.views import Response, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .serializers_rest import *
from .models import *
import datetime

class UserView(ModelViewSet):
    """
    End point for user profile, give the profile detail of logged in users
    """
    model = User
    serializer_class = UserSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.model.objects.filter(id=self.request.user.id)

    def get_user_tasks(self, task_filter=None):
        query_set = self.get_queryset()[0].task_set.all()
        return query_set

    @list_route(['get'])
    def tasks(self, request):
        """
        gives the list of tasks associated to user.
        :param request:
        :return:
        """
        tasks = self.get_user_tasks()
        serialized = TaskSerializer(tasks, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


class TaskView(ModelViewSet):
    """
    Api View for Tasks,
    requires used to be logged in for access this API.
    give all end points to access the tasks.
    """
    model = Task
    serializer_class = TaskSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        user tasks in folder wise, if folder is not mentioned, returns tasks
        which are having folder.
        :return: query set
        """
        return self.model.objects.filter(Q(owner=self.request.user) |
                                         Q(created_by=self.request.user))

    def list(self, request, *args, **kwargs):
        """
        modified the the default list function to return folder wise tasks,
        if folder is not given, list on tasks which are folder is not
        assigned
        :param request: wsgi request
        :param args:
        :param kwargs:
        :return: list of tasks as paginated
        """
        queryset = self.filter_queryset(self.get_queryset())

        folder_id = self.request.GET.get('f', None)
        if folder_id:
            queryset = queryset.filter(folder__id=folder_id)
        else:
            queryset = queryset.filter(folder__isnull=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_page_response(self, query_set, request, serializer_class):
        """
        simple function to convert query set to rest framework paginated
        response,
        :param query_set: query set
        :param request: wsgi request
        :param serializer_class: serialzer for query set
        :return: paginated response.
        """
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(query_set, request)
        serializer = serializer_class(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def perform_create(self, serializer):
        """
        on create updating created by and modified by, if owner is not
        provider it will be updated logged in user
        :param serializer:
        :return:
        """
        instance = ''
        if 'owner' not in serializer.data:
            instance = serializer.save(owner=self.request.user,
                                       created_by=self.request.user,
                                       modified_by=self.request.user)
        else:
            instance = serializer.save(created_by=self.request.user,
                                       modified_by=self.request.user)
        tags = self.request.DATA.getlist('tags')
        if tags:
            for tag in tags:
                tag_obj = Tags.objects.get_or_create(name=tag,
                                                     user=self.request.user)
                instance.tags.add(tag_obj[0])

    def perform_update(self, serializer):
        """
        on update modified by will be updated
        :param serializer:
        :return:
        """
        instance = serializer.save(mofidied_by=self.request.user)
        instance.tags.clear()
        tags = self.request.DATA.getlist('tags')
        if tags:
            for tag in tags:
                tag_obj = Tags.objects.get_or_create(name=tag,
                                                     user=self.request.user)
                instance.tags.add(tag_obj[0])

    @detail_route(['get'], url_path='toggle-done')
    def toggle_done(self, request, pk, **kwargs):
        """
        simple API for change done flag of task, it will affect it's sub task
        well.
        :param request: wsgi request
        :param pk: task ID
        :param kwargs: other values
        :return: 202 - for successful update, 500 - non successful update
        """
        try:
            task = self.get_object()
            task.is_done = not task.is_done
            task.completed_date = datetime.datetime.now()
            task.modified_by = self.request.user
            task.save()
            task.task_set.update(is_done=task.is_done)
            return Response({'detail': 'Saved'},
                            status=status.HTTP_202_ACCEPTED)
        except:
            return Response({'detail': 'Error while saving'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @detail_route(['post'],url_path='move-to-folder')
    def change_folder(self, request, pk, **kwargs):
        """
        simple API for moving task to specific folder.
        It excepts a "folder" as POST argument,
        :param request: wsgi request with Post argument to which task needs
        to move
        :param pk: task id
        :param kwargs:
        :return: 202 - on successful update, 500 - on Error
        """
        try:
            folder_pk = request.POST.get('folder', None)
            folder_obj = Folder.objects.get(id=folder_pk)
            task = self.get_object()
            task.folder = folder_obj
            task.modified_by = self.request.user
            task.save()
            detail = {'detail': 'Folder changed'}
            return Response(detail, status=status.HTTP_202_ACCEPTED)
        except:
            return Response({'detail': 'Error while saving'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @detail_route(['GET'], url_path='notes')
    def notes(self, request, pk, **kwargs):
        """
        list all notes of the particular task
        :param request: wsgi request
        :param pk: tasks id
        :param kwargs: extra arguments
        :return: paginated JSON response of notes
        """
        task = self.get_object()
        notes = task.notes.all()
        return self.get_page_response(notes, request, NotesSerializer)

    @detail_route(['GET'], url_path='sub-tasks')
    def sub_tasks(self, request, pk, **kwargs):
        """
        list all the sub tasks to the particular task
        :param request: wsgi request
        :param pk: tasks id
        :param kwargs: extra arguments
        :return: paginated JSON response of tasks
        """
        task = self.get_object()
        sub_tasks_list = task.task_set.all()
        return self.get_page_response(sub_tasks_list, request, TaskSerializer)

    @detail_route(['POST'], url_path='manage-note')
    def manage_notes(self, request, pk, **kwargs):
        """
        Manages the notes, if note id provided it will be updated else new
        note will be added
        :param request:
        :param pk:
        :param kwargs:
        :return:
        """
        notes_id = request.DATA.get('noted_id', None)
        notes = request.DATA.get('notes', None)
        notes_obj = Notes()
        if notes_id:
            try:
                notes_obj = Notes.objects.get(pk=notes_id)
            except:
                pass
        if notes:
            notes_obj.task = self.get_object()
            notes_obj.notes = notes
            notes_obj.created_by = self.request.user
            notes_obj.modified_by = self.request.user
            notes_obj.save()
            serializer = NotesSerializer(notes_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'detail':'Notes value is empty'},

                            status=status.HTTP_400_BAD_REQUEST)

    @detail_route(['POST'], url_path='manage-tags')
    def manage_tags(self, request, pk, **kwargs):
        try:
            tags = request.DATA.getlist('tags')
            task_obj = self.get_object()
            task_obj.tags.clear()
            if tags:
                for tag in tags:
                    tag_obj = Tags.objects.get_or_create(name=tag,
                                                         user=self.request.user)
                    task_obj.tags.add(tag_obj[0])
            return Response({'detail': 'tags update'}, status=status.HTTP_202_ACCEPTED)
        except:
            return Response({'detail': 'Error in updating'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @list_route(['GET'], url_path='search')
    def search(self, request):
        """
        API  for searching the tasks
        :param request: API
        :return: task list as paginated response.
        """
        term = self.request.GET.get('q', '')
        if term:
            query_set = self.get_queryset()
            query_set = query_set.extra(where = ["search_index @@ "
                                                    "to_tsquery("
                                                    "'%s' )" % (term)])
            return self.get_page_response(query_set, request, TaskSerializer)
        else:
            return Response({'detail':'No Results Found'},
                            status=status.HTTP_200_OK)