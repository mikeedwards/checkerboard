'''
Created on Jun 16, 2010

@author: edwards
'''
from models import *
from django.db.models import F
from django.contrib.gis import admin
from django.contrib.gis.admin.options import OSMGeoAdmin, GeoModelAdmin
from django.contrib.admin.options import ModelAdmin
from django.contrib.gis.geos import Point
from django_extensions.admin import ForeignKeyAutocompleteAdmin
from checkerboard.spotter.models import Win
from django.conf.urls.defaults import patterns

default = Point(-73.97,40.78,srid=4326) #WGS84
default.transform(900913) #Google

class InquiryInline(admin.StackedInline):
    model = Inquiry
    exclude = ["author",]
    extra = 1
    
class StationAdmin(OSMGeoAdmin):
    default_lat = default.y
    default_lon = default.x
    default_zoom = 12
    fields = ['plot','point','title','description','time_limit','marker_icon']
    exclude = ['altitude','accuracy','altitude_accuracy','author']
    inlines = [InquiryInline,]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()
    
    def save_formset(self, request, form, formset, change=True):
        instances = formset.save(commit=False)
        
        for instance in instances:
            instance.author = request.user
            instance.save()

    
class InquiryAdmin(admin.ModelAdmin):
    exclude = ["author",]
    list_display = ["title","station","created","description"]
    search_fields = ["title","station__title"]
    list_filter = ["station"]
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()
    

class SpottingAdmin(OSMGeoAdmin):
    default_lat = default.y
    default_lon = default.x
    default_zoom = 12
    readonly_fields = ['created']
    exclude = ['altitude','accuracy','altitude_accuracy','author']
    list_filter = ['is_snapshot','in_widget']
    list_display = ['inquiry','created','taken_on','is_snapshot','in_widget','image','author']
    search_fields = ['inquiry__title','inquiry__station__title','author__username','caption']

    def queryset(self, request):
        return Spotting.objects.all()

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()
    
class QuestionAdmin(ModelAdmin):
    exclude = ['user',]
    list_display = ['body','inquiry','created','starting','ending']
    search_fields = ['body','inquiry__title','inquiry__station__title']
    actions = ['extend_month','extend_year','retire',]
    list_filter = ['starting','ending']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        obj.save()
        
    def extend_month(self, request, queryset):
        queryset.update(ending = F('ending') + datetime.timedelta(days=30))
    
    extend_month.short_description = 'Extend the question period for 30 days'
    
    def extend_year(self, request, queryset):
        queryset.update(ending = F('ending') + datetime.timedelta(days=365))
    
    extend_year.short_description = 'Extend the question period for 365 days'
    
    def retire(self, request, queryset):
        queryset.update(ending = datetime.datetime.now() - datetime.timedelta(days=1))

    retire.short_description = 'Retire the question (but do not delete)'
    

class AnswerAdmin(ModelAdmin):    
    def spotting__author(self, instance):
        full_name = instance.spotting.author.get_full_name()
        if full_name != "":
            return full_name
        else:
            return instance.spotting.author

    spotting__author.short_description = "Author"

    def spotting__inquiry(self, instance):
        return instance.spotting.inquiry.title

    spotting__inquiry.short_description = "Activity"

    def spotting__inquiry__station(self, instance):
        return instance.spotting.inquiry.station.title
    
    spotting__inquiry__station.short_description = "Station"

    def question__body(self, instance):
        return instance.question.body

    question__body.short_description = "Question"



class NumericAnswerAdmin(AnswerAdmin):
    list_display = ['spotting__author','question__body','value','spotting__inquiry__station','spotting__inquiry','created',]
    search_fields = ['spotting__author__username','spotting__author__first_name','spotting__author__last_name',
                     'question__body','value','spotting__inquiry__station__title','spotting__inquiry__title']


class BooleanAnswerAdmin(AnswerAdmin):
    list_display = ['spotting__author','question__body','value','spotting__inquiry__station','spotting__inquiry','created',]
    search_fields = ['spotting__author__username','spotting__author__first_name','spotting__author__last_name',
                     'question__body','spotting__inquiry__station__title','spotting__inquiry__title']
    list_filter = ['value']


class TextualAnswerAdmin(AnswerAdmin):
    list_display = ['spotting__author','question__body','body','spotting__inquiry__station','spotting__inquiry','created',]
    search_fields = ['spotting__author__username','spotting__author__first_name','spotting__author__last_name',
                     'question__body','body','spotting__inquiry__station__title','spotting__inquiry__title']


class BadgeAdmin(ModelAdmin):
    list_display = ['title','description']
    exclude = ('accomplishments',)


class ReviewAdmin(ForeignKeyAutocompleteAdmin):
    list_display = ['accomplishment','reviewer']
    related_search_fields = {'accomplishment':('user__username',),'reviewer':('username',)}
    
    def get_urls(self):
        urls = super(ForeignKeyAutocompleteAdmin,self).get_urls()
        search_url = patterns('',
            (r'^foreignkey_autocomplete/$', self.admin_site.admin_view(self.foreignkey_autocomplete))
        )
        return search_url + urls

class AccomplishmentAdmin(ForeignKeyAutocompleteAdmin):
    related_search_fields = {'content_type':('name',),'user':('username',)}
    
    def get_urls(self):
        urls = super(ForeignKeyAutocompleteAdmin,self).get_urls()
        search_url = patterns('',
            (r'^foreignkey_autocomplete/$', self.admin_site.admin_view(self.foreignkey_autocomplete))
        )
        return search_url + urls

    def save_model(self, request, obj, form, change):
        if not change:
            obj.reviewer = request.user
            obj.reviewed_on = datetime.datetime.now()
        obj.save()
    


class WinAdmin(ForeignKeyAutocompleteAdmin):
    pass

admin.site.register(Station,StationAdmin)
admin.site.register(Inquiry,InquiryAdmin)
admin.site.register(Spotting,SpottingAdmin)
admin.site.register(NumericQuestion,QuestionAdmin)
admin.site.register(BooleanQuestion,QuestionAdmin)
admin.site.register(TextualQuestion,QuestionAdmin)
admin.site.register(NumericAnswer,NumericAnswerAdmin)
admin.site.register(BooleanAnswer,BooleanAnswerAdmin)
admin.site.register(TextualAnswer,TextualAnswerAdmin)
admin.site.register(Badge,BadgeAdmin)
admin.site.register(Review,ReviewAdmin)
admin.site.register(Accomplishment,AccomplishmentAdmin)
admin.site.register(Win,WinAdmin)
