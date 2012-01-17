# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from checkerboard.spotter.forms import PlotForm, ReviewFormset
from checkerboard.spotter.models import Accomplishment, Badge, Station, Spotting
from django.db.models.aggregates import Count, Max
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
from django.http import HttpResponse
from django.utils import simplejson
import datetime
from checkerboard.settings import RW_INSTANCE

@login_required
def extent_add(request):
    form = PlotForm()
    return render_to_response("spotter/extent_add.html",locals())

@login_required
def users_evaluate(request):
    users = User.objects.filter(accomplishments__isnull=False).distinct().annotate(max_date = Max("accomplishments__created"),accomplishment_count = Count("accomplishments")).order_by("-max_date")
    return render_to_response("spotter/users_evaluate.html",locals(),context_instance=RequestContext(request))


@login_required
def user_evaluate(request, username):
    badges = Badge.objects.all()
    
    stations = Station.objects.all()

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

        
    user = get_object_or_404(User, username=username)
    accomplishments = Accomplishment.objects.filter(user__username=username).annotate(review_count=Count("reviews")).order_by("-created")
    for accomplishment in accomplishments:
        if accomplishment.review_count > 0:
            accomplishment.review_class = "reviewed"
        else:
            accomplishment.review_class = "unreviewed"
            
    formset = ReviewFormset()
    return render_to_response("spotter/user_evaluate.html",locals(),context_instance=RequestContext(request))

@login_required
def user_aggregate(request):
    stations = Station.objects.all()

    user = get_object_or_404(User, pk=request.user.id)
    accomplishments = Accomplishment.objects.filter(user=user).order_by("-created")    
    remote_app_server = "http://example.com"
        
    return render_to_response("spotter/user_aggregate.html",locals(),context_instance=RequestContext(request))


from django.core import serializers
    
@login_required
def timeline(request,username=None):
    spottings = Spotting.objects.filter(is_snapshot=False).order_by("-created")
    
    events = []
    
    for spotting in spottings:
        event = {}
        if spotting.image is not None:
            print spotting.image
            try:
                event['icon'] = spotting.image.thumbnail.url()
                event['image'] = spotting.image.url
            except:
                pass
            
        event['description'] = "%s" % (spotting.answer_text.replace("\n","<br/>"))

        minute = spotting.date.minute/15 * 15
        date = datetime.datetime(spotting.date.year,spotting.date.month,spotting.date.day,spotting.date.hour,minute)
        print dir(date)

        event['start'] = unicode(date)
        if spotting.inquiry is not None:
            event['title'] = "%s" % (spotting.inquiry.title)
        event['id'] = "spotting_%d" % spotting.id
        events.append(event)
    
    json = simplejson.dumps({'dateTimeFormat':'iso8601','events':events})
    json = simplejson.dumps({'dateTimeFormat':'iso8601','events':[]})
    
    return HttpResponse(json, mimetype='application/json')
