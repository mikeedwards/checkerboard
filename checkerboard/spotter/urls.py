'''
Created on Jun 17, 2010

@author: edwards
'''
from django.conf.urls.defaults import *

urlpatterns = patterns('checkerboard.spotter.views',
    url(r'^extent/add$', 'extent_add', name='spotter_extent_add'),
    url(r'^user/(?P<username>[^/]+)/evaluate/$', 'user_evaluate', name='spotter_user_evaluate'),
    url(r'^users/evaluate/$', 'users_evaluate', name='spotter_users_evaluate'),
    url(r'^user/aggregate/$', 'user_aggregate', name='spotter_user_aggregate'),
    url(r'^timeline/(?P<username>[^/]+).json$', 'timeline', name='spotter_timeline'),
    url(r'^timeline.json$', 'timeline', name='spotter_timeline'),
)
