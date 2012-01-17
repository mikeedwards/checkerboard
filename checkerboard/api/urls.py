'''
Created on Jun 22, 2010

@author: edwards
'''
from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication, OAuthAuthentication
from checkerboard.api.handlers import RecordHandler, AnonymousRecordHandler,\
    ReadingHandler, SpottingHandler, StationHandler, InquiryHandler,\
    TextualAnswerHandler, BooleanAnswerHandler, NumericAnswerHandler,\
    UserHandler

basic_auth = HttpBasicAuthentication()
oauth_auth = OAuthAuthentication()

record_handler = Resource(handler=RecordHandler,authentication=oauth_auth)
anon_record_handler = Resource(handler=AnonymousRecordHandler)

reading_handler = Resource(handler=ReadingHandler,authentication=oauth_auth)

spotting_handler = Resource(handler=SpottingHandler)
user_handler = Resource(handler=UserHandler,authentication=oauth_auth)
station_handler = Resource(handler=StationHandler)
inquiry_handler = Resource(handler=InquiryHandler)
textual_answer_handler = Resource(handler=TextualAnswerHandler)
boolean_answer_handler = Resource(handler=BooleanAnswerHandler)
numeric_answer_handler = Resource(handler=NumericAnswerHandler)

urlpatterns += patterns('',
   url(r'^spotter/user/', user_handler),
   url(r'^spotter/spotting/(?P<id>[^/]+)/', spotting_handler),
   url(r'^spotter/spottings/', spotting_handler),
   url(r'^spotter/station/(?P<id>[^/]+)/', station_handler),
   url(r'^spotter/stations/', station_handler),
   url(r'^spotter/inquiry/(?P<inquiry>[^/]+)/spottings/', spotting_handler),
   url(r'^spotter/inquiry/(?P<id>[^/]+)/', inquiry_handler),
   url(r'^spotter/inquiries/', inquiry_handler),
   url(r'^spotter/answer/text/(?P<id>[^/]+)/', textual_answer_handler),
   url(r'^spotter/answers/text/', textual_answer_handler),
   url(r'^spotter/answer/bool/(?P<id>[^/]+)/', boolean_answer_handler),
   url(r'^spotter/answers/bool/', boolean_answer_handler),
   url(r'^spotter/answer/num/(?P<id>[^/]+)/', numeric_answer_handler),
   url(r'^spotter/answers/num/', numeric_answer_handler),
)

urlpatterns += patterns(
    'piston.authentication',
    url(r'^oauth/request_token/$','oauth_request_token'),
    url(r'^oauth/authorize/$','oauth_user_auth'),
    url(r'^oauth/access_token/$','oauth_access_token'),
)
      
