'''
Created on Mar 23, 2010

@author: edwards
'''
from django import forms
from django.forms.widgets import Textarea

class UploadPhotoForm(forms.Form):
    lat = forms.FloatField()
    lon = forms.FloatField()
    title = forms.CharField(max_length=50)
    tags = forms.CharField(max_length=50,required=False)
    photo  = forms.FileField()

class UploadBlogPostForm(forms.Form):
    title = forms.CharField(max_length=50)
    body = forms.CharField(widget=Textarea)
    tags = forms.CharField(max_length=50,required=False)
