from django.conf.urls import patterns, include, url

from django.contrib import admin
import todoapp


admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'todo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include(todoapp.urls)),
    url(r'^admin/', include(admin.site.urls)),
)
