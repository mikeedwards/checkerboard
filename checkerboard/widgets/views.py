from urllib2 import HTTPError

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils import simplejson

from checkerboard.settings import CONSUMER_KEY,CONSUMER_SECRET,SIMPLEGEO_KEY,SIMPLEGEO_SECRET,REMOTE_APP_INSTANCE,spotter_GROUP_ID

from forms import UploadPhotoForm
import simplegeo
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
import random
import datetime
from checkerboard.spotter.models import Badge,Win, Station
from django.conf import settings
from checkerboard.widgets.forms import UploadBlogPostForm
import logging

sg_client = simplegeo.Client(SIMPLEGEO_KEY,SIMPLEGEO_SECRET)

def index(request):
    return render_to_response('widgets/index.html')

def frame(request):
    referer = request.META.get('HTTP_REFERER')


    request_token = request.session.get('request_token', None)
    access_token = request.session.get('access_token', None)
    
    if request_token is not None:
        logging.debug("frame view, request_token = %s " % request_token)
    else:
        logging.debug("frame view, request_token missing")
    if access_token is not None:
        logging.debug("frame view, access_token = %s " % access_token)
    else:
        logging.debug("frame view, access_token missing")

    logging.debug("frame view, user = %s" % request.user)
    
    

    if access_token is None:
        request.session['next'] = reverse("widgets_frame")
        request.session['initial_referer'] = referer
        return HttpResponseRedirect(reverse("widgets_public_frame"))
        # we're redirecting to a public frame for now
        #return login(request)

    initial_path = None

    if request.session.has_key('initial_referer'):
        initial_referer = request.session['initial_referer']
        if request.session['initial_referer'] is not None:
            initial_path = request.session['initial_referer'].split('/')

    if referer:
        referer_path = referer.split('/')

        group_id = None
    
        if referer_path[-2] == "groups":
            group_id = referer_path[-1]
        elif initial_path is not None and initial_path[-2] == "groups":
            group_id = initial_path[-1]

        if group_id is not None:
            wins = Win.objects.filter(complete = True).order_by("-created")[:5]


    return render_to_response('widgets/frame.html',locals(),context_instance=RequestContext(request))

def widget(request):
    now = datetime.datetime.now()
    users = User.objects.filter(spotter_spottings__isnull = False).distinct()
    stations = Station.objects.all()
    return render_to_response('widgets/widget.html',locals(),context_instance=RequestContext(request))

def map(request):
    referer = request.META.get('HTTP_REFERER')

    access_token = request.session.get('access_token', None)

    if access_token is None:
        request.session['next'] = reverse("widgets_map")
        request.session['initial_referer'] = referer
        return HttpResponseRedirect(reverse("widgets_public_frame"))

    key = settings.GOOGLE_MAPS_KEY
    users = User.objects.filter(spotter_spottings__isnull = False).distinct()
    stations = Station.objects.all()
    now = datetime.datetime.now()
    return render_to_response('widgets/map.html',locals(),context_instance=RequestContext(request))

def badge_summary(request):
    badges = Badge.objects.all().order_by("title")
    return render_to_response('widgets/badge_summary.html',locals(),context_instance=RequestContext(request))

def badges(request):
    referer = request.META.get('HTTP_REFERER')

    username = None
    if referer is not None and referer.find('people/') > 0:
        username = referer.split("-")[-1]

    if request.session.has_key('initial_referer'):
        initial_referer = request.session['initial_referer']

    if username is not None:
        wins = Win.objects.filter(user__username = username,complete = True)
    elif request.user.is_authenticated():
        wins = Win.objects.filter(user=request.user, complete = True)
    return render_to_response('widgets/badges.html',locals(),context_instance=RequestContext(request))

def public_frame(request):
    referer = request.META.get('HTTP_REFERER')
    request.session.set_test_cookie()

    if referer:
        referer_path = referer.split('/')

        group_id = None
    
        initial_path = None

        if request.session.has_key('initial_referer'):
            initial_referer = request.session['initial_referer']
            if request.session['initial_referer'] is not None:
                initial_path = request.session['initial_referer'].split('/')

        if referer_path[-2] == "groups":
            group_id = referer_path[-1]
        elif initial_path is not None and initial_path[-2] == "groups":
            group_id = initial_path[-1]

    response = render_to_response('widgets/public_frame.html',locals(),context_instance=RequestContext(request))
    response["P3P"] = 'CP="IDC DSP COR ADM DEVi TAIi PSA PSD IVAi IVDi CONi HIS OUR IND CNT"'
    return response

def safari_no_cookie(request):
    redirect_to = request.GET.get("redirect_to")
    return HttpResponseRedirect(redirect_to);

def login(request):
    request.session['request_token'] = None
    request.session['auth_url'] = None
    request.session['access_token'] = None
    
    request_token = remote_app_client.fetch_request_token(callback=request.build_absolute_uri(reverse("widgets_return")))
    request.session['request_token'] = request_token
        
    next = request.GET.get('next',None)
    if next is not None:
        request.session['next'] = next
    
    auth_url = remote_app_client.authorize_token_url(request_token)
    request.session['auth_url'] = auth_url
        
    return HttpResponseRedirect(auth_url)

        
def logout(request):
    request.session['request_token'] = None
    request.session['auth_url'] = None
    request.session['access_token'] = None
    if request.user.is_authenticated():
        auth_logout(request)

    next = request.GET.get('next',None)
    if next is not None:
        request.session['next'] = next
        return HttpResponseRedirect(reverse("widgets_login") + "?next=" + next)
    else:
        return HttpResponseRedirect(reverse("widgets_login"))        
        
def logout_mobile(request):
    request.session['request_token'] = None
    request.session['auth_url'] = None
    request.session['access_token'] = None
    auth_logout(request)
    
    next = request.GET.get('next',None)
 
    if next is not None:
        return HttpResponseRedirect(next)
    else:    
        return HttpResponseRedirect(reverse("widgets_login"))

def _return(request):
    
    verifier = request.GET.get('oauth_verifier',None)
    logging.debug("_return view, verifier = %s " % verifier)
    request_token = request.session.get('request_token', None)
    initial_referer = request.session.get('initial_referer', None)
    next = request.session.get('next', None)

    if request_token is not None:
        logging.debug("_return view, request_token = %s " % request_token)
    else:
        logging.debug("_return view, request_token missing")
        
    print next

    if request_token is None:
        message = "No request token!"
    else:
        access_token = remote_app_client.fetch_access_token(request_token, verifier=verifier, callback=request.build_absolute_uri(reverse("widgets_return")))
        if access_token is not None:
            logging.debug("_return view, access_token = %s " % access_token)
        else:
            logging.debug("_return view, access_token missing")
        
        request.session['access_token'] = access_token
        message = "Access token key = %s " % (access_token.key)

        url = "/api/v1/people/current.json"
    
        user_data = simplejson.loads(remote_app_client.request_url(access_token, url, {}, "GET"))
        username = user_data['name']
        first_name = user_data['first_name']
        last_name = user_data['last_name']
        email = user_data['email']
        id = user_data['id']
        
        try:
            user = User.objects.get(username=username)
        except:
            user = User.objects.create_user(username, email, "".join([chr(random.randrange(48,123)) for i in range(20)]))
            user.first_name = first_name
            user.last_name = last_name
        user.backend='django.contrib.auth.backends.ModelBackend' 
        auth_login(request,user)
        
        logging.debug("_return view, user = %s " % request.user)
        
    
    if next is not None:
        response =  HttpResponseRedirect(next)
    else:
        response =  HttpResponseRedirect(reverse("widgets_frame"))
    response["P3P"] = 'CP="IDC DSP COR ADM DEVi TAIi PSA PSD IVAi IVDi CONi HIS OUR IND CNT"'
    return response
    
def photos(request):
    request_token = request.session.get('request_token', None)

    access_token = request.session.get('access_token', None)

    if request_token is None:
        request_token = remote_app_client.fetch_request_token(callback=request.build_absolute_uri(reverse("widgets_return")))
        request.session['request_token'] = request_token

    if access_token is None:
        access_token = remote_app_client.fetch_access_token(request_token,callback=request.build_absolute_uri(reverse("widgets_return")))
        request.session['access_token'] = access_token
    
    parameters = {}
    url = "/api/v1/photos.json"

    photos_json = remote_app_client.request_url(access_token, url, parameters, "GET")

    return render_to_response('widgets/photos.html',locals())

def photo(request,id):
    request_token = request.session.get('request_token', None)

    access_token = request.session.get('access_token', None)

    if request_token is None:
        request_token = remote_app_client.fetch_request_token(callback=request.build_absolute_uri(reverse("widgets_return")))
        request.session['request_token'] = request_token

    if access_token is None:
        access_token = remote_app_client.fetch_access_token(request_token,callback=request.build_absolute_uri(reverse("widgets_return")))
        request.session['access_token'] = access_token
    
    parameters = {}
    url = "/api/v1/photos/%s.json" % (id)

    photo_json = remote_app_client.request_url(access_token, url, parameters, "GET")
    photo = simplejson.loads(photo_json)
    
    layer = "layer_name"
    
    photo_id = "photos.%s" % (photo['id'])
            
    record = sg_client.get_record(layer,photo_id)

    return render_to_response('widgets/photo.html',locals())

def upload_blog_post(request):
    response_json = ""
    if request.method == 'POST':
        form = UploadBlogPostForm(request.POST)
        if form.is_valid():
            tags = form.cleaned_data['tags']
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']

            access_token = request.session.get('access_token', None)
        
            parameters = {'blog_post[title]': title, 'blog_post[tags]': tags, 'blog_post[body]': body, 'blog_post[publish]': True} # resource specific params
                
            if access_token is not None:
                response_json = remote_app_client.request_url(access_token, url, parameters, "POST")
            else:
                response_json = simplejson.dumps({'status':'403','message':'Permission denied'})
                                
    return HttpResponse(response_json, mimetype='application/json')


def upload_file(request):
    if request.method == 'POST':
        form = UploadPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            tags = form.cleaned_data['tags']
            title = form.cleaned_data['title']
            photo = form.cleaned_data['photo']
            lat = form.cleaned_data['lat']
            lon = form.cleaned_data['lon']
            
            request_token = request.session.get('request_token', None)
        
            access_token = request.session.get('access_token', None)
        
            if request_token is None:
                request_token = remote_app_client.fetch_request_token(callback=request.build_absolute_uri(reverse("widgets_return")))
                request.session['request_token'] = request_token
        
            if access_token is None:
                access_token = remote_app_client.fetch_access_token(request_token,callback=request.build_absolute_uri(reverse("widgets_return")))
                request.session['access_token'] = request_token
    
            parameters = {'photo[title]': title, 'photo[tags]': tags, 'photo[photo]': photo} # resource specific params

            url = "layer_name"    
    
            response_json = remote_app_client.request_url(access_token, url, parameters, "POST")
            
            try:
                response = simplejson.loads(response_json)
            except:
                response = response_json
                return render_to_response('widgets/upload.html', 
                              locals(), 
                              context_instance=RequestContext(request))
                
            
            layer = "layer_name"
            
            photo_id = "photos.%s" % (response['id'])
            
            photo_location_record = simplegeo.Record(layer,photo_id,lat,lon,type='image')
            
            sg_client.add_record(photo_location_record)
            
            return HttpResponseRedirect(reverse("widgets_photo",kwargs={'id':response['id']}))
        
    else:
        form = UploadPhotoForm()
    return render_to_response('widgets/upload.html', 
                              locals(), 
                              context_instance=RequestContext(request))
