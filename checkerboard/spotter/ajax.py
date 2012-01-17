'''
Created on Jul 18, 2010

@author: edwards
'''
from django.utils import simplejson
from dajax.core import Dajax
from dajaxice.core import dajaxice_functions
from checkerboard.spotter.models import Accomplishment, Badge, Win, Review, Spotting,\
    Inquiry
from django.core import serializers
from django.template.defaultfilters import timesince
from django.db.models import Q
import datetime
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.contrib.gis.db.models.query import GeoQuerySet
from django.core.mail import send_mail

def count(request,username):
    dajax = Dajax()
    accomplishments = Accomplishment.objects.filter(user__username=username).count()
    dajax.assign('#count','innerHTML',str(accomplishments))
    return dajax.json()
    

def filter(request,username,station=0,type="all",time=0):
    dajax = Dajax()
    
    query = [Q(user__username=username)]

    if time != 0:
        query.append(Q(created__gt = datetime.datetime.now() - datetime.timedelta(days = time)))

    if type != "all":
        query.append(Q(content_type__name=type))

    accomplishments_all = Accomplishment.objects.filter(*query).order_by("-created")
        
    if station == 0:
        accomplishments = accomplishments_all
    else:
        accomplishments = []
        
        for accomplishment in accomplishments_all:
            if accomplishment.station is not None and accomplishment.station.id == station:
                accomplishments.append(accomplishment)    
        
    data = serialize_accomplishments(accomplishments)
    dajax.add_data(data, "filter_callback")
    return dajax.json()
        
def post_accomplishments(request,badge,username,data):
    dajax = Dajax()
    
    if request.user.is_authenticated():
        badge = Badge.objects.get(pk=badge)
        
        user = User.objects.get(username = username)
    
        for id in data:
            acc = Accomplishment.objects.get(pk=id)
            badge.accomplishments.add(acc)
            review = Review.objects.get_or_create(reviewer=request.user,accomplishment=acc)[0]
            review.modified = datetime.datetime.now()
            review.save()
    
        win = Win.objects.get_or_create(badge=badge,user=user)[0]

        accomplishments = badge.accomplishments.filter(user__username = username).order_by("-created")
        
        a_data = serialize_accomplishments(accomplishments)
        
        dajax.add_data({'badge':badge.id,'a_data':a_data}, "badge_accomplishments_callback")

    return dajax.json()

def clear_accomplishments(request,badge,username,data):
    dajax = Dajax()
    
    if request.user.is_authenticated():
        badge = Badge.objects.get(pk=badge)
        
        user = User.objects.get(username = username)
    
        for id in data:
            acc = Accomplishment.objects.get(pk=id)
            badge.accomplishments.remove(acc)
            reviews = Review.objects.filter(reviewer=request.user,accomplishment=acc)
            for review in reviews:
                review.delete()
    
        win = Win.objects.get(badge=badge,user=user)
        win.complete=False
        win.save()

        accomplishments = badge.accomplishments.filter(user__username = username).order_by("-created")
        
        a_data = serialize_accomplishments(accomplishments)
        
        dajax.add_data({'badge':badge.id,'a_data':a_data}, "badge_accomplishments_callback")

    return dajax.json()

def award_badge(request,badge, username):
    dajax = Dajax()

    badge = Badge.objects.get(pk=badge)
    user = User.objects.get(username = username)
    
    win = Win.objects.get_or_create(badge=badge,user=user)[0]
    win.complete=True
    if not win.email_sent:
        send_mail("You earned the spotter %s badge!" % (badge.title),
                  """%s\nBe sure to check back with your profile for more updates!""" % (badge.email_description),
                  "admin@example.com",
                  [user.email],
                  fail_silently=True)
        win.email_sent = True
    win.save()
    
    return refresh_badges(request,username,True)

def refresh_badges(request,username,reset=False):
    dajax = Dajax()

    dajax.assign('#badges tbody','innerHTML',"")
    
    badges = Badge.objects.all()
    
    for badge in badges:
        badge.user_accomplishments = badge.accomplishments.filter(user__username = username)
        win = badge.wins.filter(user__username=username)
        print win
        if len(win) == 0:
            badge.status = "open"
        elif win[0].complete:
            badge.status = "completed"
        else:
            badge.status = "in progress"
        
        badge_html = """   
              <tr class="badge" id="badge_%d">
                  <td width="50">
                      <img src="%s" title="%s" width="48" height="48"/>
                  </td>
                  <td>
                      <div class="badge_title"><nobr>%s</nobr></div>
                      <div class="status-%s">%s</div>
                  </td>
              </tr>
              """ % (badge.id,badge.image.thumbnail.url(),badge.description,badge.title,badge.status.lower().replace(" ","-"),badge.status)

        dajax.append('#badges tbody','innerHTML',badge_html)
        if reset:
            dajax.script("$('.badge_review_section').addClass('hide_badge_reviews')");
        dajax.script("$('.badge').click(click_badge)");

    return dajax.json()


def request_points(request,username='',station='',inquiry=''):
    dajax = Dajax()
    
    query = [Q(in_widget=True),Q(image__isnull=False)]
    #query = [Q(image__isnull=False)]

    inquiry_id = "-1"
    
    if username != '':        
        query.append(Q(author__username=username))
    if inquiry != '':
        query.append(Q(inquiry__id=inquiry))
        inquiry_id = inquiry
    if station != '':
        query.append(Q(inquiry__station__id=station))
        inquiries = Inquiry.objects.filter(station__id=station)
        inquiryHTML = "<option value=\"\">--All--</option>"
        for inquiry in inquiries:
            if int(inquiry_id) == inquiry.id:
                inquiryHTML += "<option value=\"%d\" selected=\"true\">%s</option>" % (inquiry.id,inquiry.title)
            else:
                inquiryHTML += "<option value=\"%d\">%s</option>" % (inquiry.id,inquiry.title)
        dajax.assign('#inquirySelect','innerHTML',inquiryHTML)
    
    spottings = Spotting.objects.filter(*query).order_by("-created")
    collect = spottings.collect()
    if collect is not None:
        last = spottings[0].created
        cc = collect.centroid
        ce = collect.extent
    
        center = {'lat':cc.y,'lng':cc.x}
    
        events = []
    
        for spotting in spottings:
            if spotting.image is not None:
                try:
                    answers = []
                    for answer in spotting.answers.all():
                        try:
                            text = "%s" % getattr(answer,"textualanswer",None).body
                        except answer.DoesNotExist:
                            pass
                        
                        try:
                            text = "%d" % getattr(answer,"numericanswer",None).value
                        except answer.DoesNotExist:
                            pass
                        
                        try:
                            test = getattr(answer,"booleananswer",None).value
                            if test:
                                text = answer.question.true_text
                            else:
                                text = answer.question.false_text
                        except answer.DoesNotExist:
                            pass

                        answers.append({'question':answer.question.body,'answer':text})
                        
                    if spotting.author.get_full_name() != "":
                        author = spotting.author.get_full_name()
                    else:
                        author = spotting.author.username
                    

                    events.append({'id':"event%d" % spotting.id,
                                   'author': author,
                                   'lat':spotting.point.y,
                                   'lng':spotting.point.x,
                                   'title':timesince(spotting.date) + " ago",
                                   'start':unicode(spotting.date),
                                   'since':timesince(spotting.date),
                                   'text':spotting.answer_text,
                                   'caption':spotting.caption,
                                   'answers':answers,
                                   'image':spotting.image.url,
                                   'thumbnail':spotting.image.thumbnail.url()})
                except:
                    pass
        if (len(events) > 0):
            dajax.add_data({'dateTimeFormat':'iso8601',
                            'center':center,
                            'bounds':ce,
                            'last':unicode(last),
                            'events':events},'draw_points')
            dajax.assign('#messageDisplay','innerHTML',"%d observations loaded..." % (len(events)))
            return dajax.json()

    dajax.assign('#messageDisplay','innerHTML',"No observations found")
        
    return dajax.json()
      
      
def move_point(request, lat, lng):
    dajax = Dajax()
    message = "Saved new location at, %s, %s" % (lat, lng)
    dajax.assign('#example_log','value',message)
    return dajax.json()

dajaxice_functions.register(request_points)
dajaxice_functions.register(move_point)
        
dajaxice_functions.register(filter)
dajaxice_functions.register(post_accomplishments)
dajaxice_functions.register(clear_accomplishments)
dajaxice_functions.register(award_badge)
dajaxice_functions.register(refresh_badges)

def serialize_accomplishments(accomplishments):
    data = []
    for accomplishment in accomplishments:
        data.append({'id':accomplishment.id, 'type':accomplishment.content_type.name, 'station':accomplishment.station.title, 'inquiry':accomplishment.inquiry.title, 'content':accomplishment.content, 'created':timesince(accomplishment.created)})
    return data
    

