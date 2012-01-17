from django.conf.urls.defaults import *

urlpatterns = patterns('checkerboard.widgets.views',
    url(r'^$', 'index', name='widgets_index'),
    url(r'^upload/file/$', 'upload_file', name='widgets_upload_file'),
    url(r'^upload/blog_post/$', 'upload_blog_post', name='widgets_upload_blog_post'),
    url(r'^badges/$', 'badges', name='widgets_badges'),
    url(r'^badge_summary/$', 'badge_summary', name='widgets_badge_summary'),
    url(r'^login/$', 'login', name='widgets_login'),
    url(r'^logout/$', 'logout', name='widgets_logout'),
    url(r'^return/$', '_return', name='widgets_return'),
    url(r'^photos/$', 'photos', name='widgets_photos'),
    url(r'^photo/(?P<id>[0-9]+)$', 'photo', name='widgets_photo'),
    url(r'^public/$', 'public_frame', name='widgets_public_frame'),
    url(r'^widget/$', 'widget', name='widgets_widget'),
    url(r'^map/$', 'map', name='widgets_map'),
    url(r'^safari_no_cookie/$', 'safari_no_cookie', name='widgets_safari_no_cookie'),
)
