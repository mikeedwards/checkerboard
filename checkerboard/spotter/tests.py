"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from checkerboard.community.models import Plot
from checkerboard.spotter.models import Station, Spotting
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import Polygon

class PlotTest(TestCase):
    
    def setUp(self):
        self.user_mentor = User.objects.create_user("test_mentor", "test_mentor@example.com", "test")
        self.user_mentor.first_name = "First"
        self.user_mentor.last_name = "Last"
        self.user_mentor.save()
        #self.mentor = Mentor.objects.create(user=self.user_mentor)

        self.user_learner = User.objects.create_user("test_learner", "test_learner@example.com", "test")
        self.user_learner.first_name = "First"
        self.user_learner.last_name = "Last"
        self.user_learner.save()
        #self.learner = Learner.objects.create(user=self.user_learner)
    
    def test_add_plot(self):
        """
        Tests we can add an plot.
        """
        self.create_plot()
        
        plot = Plot.objects.get(title = "This is a test plot")
        
        self.failUnless(plot.center.y < 40.9, "Center latitude not less than NE corner")
        self.failUnless(plot.center.y > 40.8, "Center latitude not greater than SW corner")
        
    def test_add_station(self):
        plot, station = self.create_station()

        self.failUnless(station in plot.stations.all(), "Stations not found in the plot")
                
    def test_add_spotting(self):
        station = self.create_station()[1]
    
        spotting = Spotting.objects.get_or_create(station=station,
                                                  author = self.user_learner,
                                                  point=station.point)[0]
                
        self.failUnless(spotting in self.user_learner.spottings.all(), "Spotting not found for the learner")
        self.failUnless(station in self.user_learner.investigated_stations.all(), "Stations not connected to learner through spotting")
    
    def create_plot(self):
        polygon = Polygon(((-75.1,40.9),(-75.1,40.8),(-75.0,40.8),(-75.0,40.8),(-75.1,40.9)))
        plot = Plot.objects.get_or_create(author = self.user_mentor,
                                              polygon = polygon,
                                              title = "This is a test plot")[0]
        #print Plot.objects.kml()[0].kml
        
        return plot

    def create_station(self):
        plot = self.create_plot()
        station = Station.objects.get_or_create(plot=plot, 
            author=plot.author, 
            title="This is a test station", 
            description="This is what we say about that!",
            point=Point(plot.center[0],plot.center[1])
            )[0]
        return plot, station

    
        

        
        

