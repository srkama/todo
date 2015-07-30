__author__ = 'kamal.s'
from rest_framework.routers import DefaultRouter
from django.conf.urls import patterns, include, url

from .api_rest import *

api = DefaultRouter()
api.register(r'profile', UserView, 'profile')
api.register(r'tasks', TaskView, 'task')


urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'angularjs.views.home', name='home'),
                       url(r'api/', include(api.urls)),
                       )