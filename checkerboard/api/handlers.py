'''
Created on Jun 22, 2010

@author: edwards
'''
import re

from piston.handler import BaseHandler,AnonymousBaseHandler
from piston.utils import rc, throttle

from django.contrib.auth.models import User
from checkerboard.community.models import Plot
from django.contrib.gis.geos import Point,Polygon
from checkerboard.spotter.models import Spotting,Station, Inquiry, TextualAnswer,\
    Question, BooleanAnswer, NumericAnswer
from django.core.files import File
from django.contrib.gis.measure import Distance

class UserHandler(BaseHandler):
    allowed_methods = ('GET',)
    fields = ('id',
              'username',)
    model = User
    
    def read(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return request.user
        else:
            return None


class SpottingHandler(BaseHandler):
    allowed_methods = ('GET','POST','PUT', 'DELETE',)
    fields = ('id',
              'image_url',
              'latlon',
              'date',
              'created',
              'modified',
              'caption',
              ('inquiry',
                ('id',
                 'title',
                 'description',
                 'long_description',
                 'instructions',
                 'payoff',)),
              ('author',
                ('username',)),
              ('answers',
                ("value_text",
                 ('question',
                  ('body',)))),
              )

    model = Spotting
    by_inquiry = False

    @classmethod
    def content_size(self, spotting):
        return len(spotting.content)

    def queryset(self, request):
        if not self.by_inquiry:
            return self.model.objects.reverse()
        else:
            return self.model.snapshots.reverse() 

    def create(self, request, id=None, inquiry_id=None):
        """
        Tested with:
        curl -u edwards:test -X POST -F inquiry.id="1" -F author.username="edwards" -F image=@/home/edwards/Pictures/profile.jpg -F latlon.lon="-75.1" -F latlon.lat="40.7" http://127.0.0.1:8000/api/spotter/spottings/
        """
        spotting = Spotting()
        print request.POST
        spotting.inquiry = Inquiry.objects.get(id=int(request.POST.get('inquiry.id')))
        if request.user.is_authenticated():
            spotting.author = request.user
        elif request.POST.get('author.username') is not None:
            user = User.objects.get(username=request.POST.get('author.username'))
            spotting.author = user
        else:
            return None
        lat = request.POST.get('latlon.lat')
        lon = request.POST.get('latlon.lon')
        spotting.caption = request.POST.get('caption')
        spotting.point = "POINT(%s %s)" % (lon,lat)
        spotting.image = File(request.FILES.get('image'))
        spotting.save()

        return spotting
    
    def read(self, request, *args, **kwargs):
        if kwargs.has_key('inquiry'):
            self.by_inquiry = True
        return super(SpottingHandler,self).read(request,*args,**kwargs)
            
    
class TextualAnswerHandler(BaseHandler):
    allowed_methods = ('GET','POST',)
    fields = ('id',
              'body',
              ('spotting',('id',)),
              ('question',('id',)),
              )
    model = TextualAnswer

    def create(self, request, id=None):
        answer = TextualAnswer()
        spotting = Spotting.objects.get(id=int(request.POST.get('spotting')))
        question = Question.objects.get(id=int(request.POST.get('question')))
        answer.body = request.POST.get('body')
        answer.spotting = spotting
        answer.question = question
        answer.save()
        
        return answer

class BooleanAnswerHandler(BaseHandler):
    allowed_methods = ('GET','POST',)
    fields = ('id',
              'value',
              ('spotting',('id',)),
              ('question',('id',)),
              )
    model = BooleanAnswer

    def create(self, request, id=None):
        answer = BooleanAnswer()
        spotting = Spotting.objects.get(id=int(request.POST.get('spotting')))
        question = Question.objects.get(id=int(request.POST.get('question')))
        if request.POST.get('value') == 'true':
            answer.value = True
        else:
            answer.value = False
            
        answer.spotting = spotting
        answer.question = question
        answer.save()
        
        return answer

class NumericAnswerHandler(BaseHandler):
    allowed_methods = ('GET','POST',)
    fields = ('id',
              'value',
              ('spotting',('id',)),
              ('question',('id',)),
              )
    model = NumericAnswer

    def create(self, request, id=None):
        answer = NumericAnswer()
        spotting = Spotting.objects.get(id=int(request.POST.get('spotting')))
        question = Question.objects.get(id=int(request.POST.get('question')))
        answer.value = int(request.POST.get('value'))
        answer.spotting = spotting
        answer.question = question
        answer.save()
        
        return answer

class StationHandler(BaseHandler):
    allowed_methods = ('GET',)
    fields = ('id',
              'title',
              'description',
              'marker_icon_url',
              ('plot',('id',
                       'title')),
              ('inquiries',
                ('id',
                 'title',
                 'description',
                 'long_description',
                 'instructions',
                 'payoff',)),
              'latlon',
              'time_limit',
              )
    
    model = Station
  
    @classmethod
    def content_size(self, station):
        return len(station.content)

    def queryset(self,request):
        if request.GET.get("lat",None) is not None:
            lat = float(request.GET.get("lat",None))
            lon = float(request.GET.get("lon",None))
            pnt = Point(lon,lat)
            return self.model.objects.filter(point__distance_lt=(pnt,Distance(km=5))).distance(pnt).order_by("distance")
        else:
            return self.model.objects.all()


    def read(self,request,*args,**kwargs):
            
        return super(StationHandler,self).read(request,*args,**kwargs)

class InquiryHandler(BaseHandler):
    allowed_methods = ('GET',)
    fields = ('id',
              'title',
              'description',
              'long_description',
              'instructions',
              'payoff',
              ('questions',
                ('id',
                 'body',
                 'field_dict',)),
              ('spottings',
                ('id',
                 'image_url',
                 'taken_on',
                 'latlon',)),
              ('station',
                ('id',
                 'title',
                 'description',)),
              )
    
    model = Inquiry
  
    @classmethod
    def content_size(self, inquiry):
        return len(inquiry.content)
    
class ArbitraryDataHandler(BaseHandler):
    methods_allowed = ('GET',)

    def read(self, request, username, data):
        user = User.objects.get(username=username)

        return { 'user': user, 'data_length': len(data) }
