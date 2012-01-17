from django.db import models
from django.contrib.auth.models import User
from django_extensions.db.models import TimeStampedModel
from django.contrib.gis.db.models.fields import PointField, PolygonField
from django.contrib.gis.db.models.manager import GeoManager

class Profile(TimeStampedModel):
    user = models.ForeignKey(User, unique=True)

    def __unicode__(self):
        return self.user.username

class Role(models.Model):
    profile = models.OneToOneField(Profile, blank=True, unique=True, related_name="%(class)s")

    class Meta:
        abstract = True
        
    def __unicode__(self):
        return self.profile

class Learner(Role):
    pass

class Mentor(Role):
    pass

from south.modelsinspector import add_introspection_rules #@UnresolvedImport

from django.contrib.gis.geos import Point, Polygon

add_introspection_rules([], ["^django_extensions\.db\.fields"])

class LocativeModel(TimeStampedModel):
    point = PointField()
    altitude = models.FloatField(blank=True,null=True)
    accuracy = models.FloatField(blank=True,null=True)
    altitude_accuracy = models.FloatField(blank=True,null=True)
    
    objects = GeoManager()
    
    class Meta(TimeStampedModel.Meta):
        abstract = True

    def latlon(): #@NoSelf
        doc = """Returns the latitude/longitude pair as a dict for the API, etc.""" #@UnusedVariable
       
        def fget(self):
            #return self.point.geojson
            return {'lat':self.point.y,'lon':self.point.x}
              
        return locals()
       
    latlon = property(**latlon())
    

class AreaModel(TimeStampedModel):
    polygon = PolygonField()

    objects = GeoManager()

    class Meta(TimeStampedModel.Meta):
        abstract = True
        
    def get_center(self):
        return self.polygon.centroid
    
    def center(): #@NoSelf
        doc = """The center latitude and longitude of the area.  This is only accurate for very small geographic areas.""" #@UnusedVariable
       
        def fget(self):
            return self.get_center()
           
        return locals()
       
    center = property(**center())

class Plot(AreaModel):
    author = models.ForeignKey(User, related_name="authored_plots")
    title = models.CharField(max_length=50)
    description = models.TextField(null=True,blank=True)

    def __unicode__(self):
        return self.title

