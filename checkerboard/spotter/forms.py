'''
Created on Jun 17, 2010

@author: edwards
'''
from django.forms.models import ModelForm, modelformset_factory
from checkerboard.spotter.models import Plot, Review
from django.contrib.gis.admin.widgets import OpenLayersWidget
from django.forms.widgets import Textarea
from django.contrib.gis.gdal.geomtype import OGRGeomType
from django import forms
from django.forms.formsets import formset_factory

class ReviewForm(forms.Form):
    approve = forms.BooleanField()
    notes = forms.CharField(widget=forms.Textarea)
        
ReviewFormset = formset_factory(ReviewForm)

class MapWidget(OpenLayersWidget):
    default_lat = 0
    default_lon = 0
    default_zoom = 4
    display_wkt = False
    display_srid = False
    num_zoom = 18
    max_zoom = False
    min_zoom = False
    max_extent = False
    modifiable = True
    mouse_position = True
    scale_text = True
    layerswitcher = True
    scrollable = True
    map_width = 600
    map_height = 400
    map_template = 'gis/admin/osm.html'
    openlayers_url = 'http://openlayers.org/api/2.8/OpenLayers.js'
    point_zoom = num_zoom - 6
    wms_url = 'http://labs.metacarta.com/wms/vmap0'
    wms_layer = 'basic'
    wms_name = 'OpenLayers WMS'
    debug = False
    #OSM properties
    extra_js = ['http://openstreetmap.org/openlayers/OpenStreetMap.js']
    num_zoom = 20
    map_srid = 900913
    max_extent = '-20037508,-20037508,20037508,20037508'
    max_resolution = 156543.0339
    units = 'm'
        
    def __init__(self,*args,**kwargs):
        super(MapWidget, self).__init__(*args,**kwargs)
        
        self.template = self.map_template
        self.geom_type = "POLYGON"
        self.params = {'default_lon' : self.default_lon,
                  'default_lat' : self.default_lat,
                  'default_zoom' : self.default_zoom,
                  'display_wkt' : self.debug or self.display_wkt,
                  'geom_type' : OGRGeomType(self.geom_type),
                  'field_name' : "polygon",
                  'is_collection' : False,
                  'scrollable' : self.scrollable,
                  'layerswitcher' : self.layerswitcher,
                  'collection_type' : 'None',
                  'is_linestring' : self.geom_type in ('LINESTRING', 'MULTILINESTRING'),
                  'is_polygon' : self.geom_type in ('POLYGON', 'MULTIPOLYGON'),
                  'is_point' : self.geom_type in ('POINT', 'MULTIPOINT'),
                  'num_zoom' : self.num_zoom,
                  'max_zoom' : self.max_zoom,
                  'min_zoom' : self.min_zoom,
                  'units' : self.units, #likely shoud get from object
                  'max_resolution' : self.max_resolution,
                  'max_extent' : self.max_extent,
                  'modifiable' : self.modifiable,
                  'mouse_position' : self.mouse_position,
                  'scale_text' : self.scale_text,
                  'map_width' : self.map_width,
                  'map_height' : self.map_height,
                  'point_zoom' : self.point_zoom,
                  'srid' : self.map_srid,
                  'display_srid' : self.display_srid,
                  'wms_url' : self.wms_url,
                  'wms_layer' : self.wms_layer,
                  'wms_name' : self.wms_name,
                  'debug' : self.debug,
                  }

class PlotForm(ModelForm):
    class Meta:
        model = Plot
        widgets = {'polygon':MapWidget}
        
    default_lon = 0
    
