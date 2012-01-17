'''
Created on Jun 17, 2010

@author: edwards
'''
from models import *
from django.contrib import admin
from django.contrib.gis.admin.options import OSMGeoAdmin, GeoModelAdmin
from django.contrib.admin.options import ModelAdmin

default = Point(-73.97,40.78,srid=4326) #WGS84
default.transform(900913) #Google

class PlotAdmin(OSMGeoAdmin):
    default_lat = default.y
    default_lon = default.x
    default_zoom = 12
    exclude = ['author',]
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()
    
admin.site.register(Mentor)
admin.site.register(Learner)

admin.site.register(Plot,PlotAdmin)