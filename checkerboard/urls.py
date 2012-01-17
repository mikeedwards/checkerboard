from django.conf import settings

from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

from dajaxice.core import dajaxice_autodiscover
dajaxice_autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^checkerboard/', include('checkerboard.widgets.urls')),

    (r'^spotter/', include('checkerboard.spotter.urls')),

    (r'^api/', include('checkerboard.api.urls')),

    (r'^admin/', include(admin.site.urls)),
    
    url(r'^accounts/login', 'checkerboard.widgets.views.login', name='widgets_login'),
    
    url(r'^accounts/logout_mobile', 'checkerboard.widgets.views.logout_mobile', name='widgets_logout_mobile'),
    
    url(r'^accounts/logout', 'checkerboard.widgets.views.logout', name='widgets_logout'),
    
    url(r'^$', 'checkerboard.widgets.views.index', name='widgets_index_root'),

    url(r'^frame/$', 'checkerboard.widgets.views.frame', name='widgets_frame'),
    
    (r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),
)
