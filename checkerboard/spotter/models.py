from django.db import models
from django_extensions.db.models import TimeStampedModel,TitleSlugDescriptionModel
from django_extensions.db.fields import AutoSlugField
from checkerboard.community.models import User, LocativeModel, Plot
from south.modelsinspector import add_introspection_rules #@UnresolvedImport
import checkerboard
import datetime
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from stdimage.fields import StdImageField
from django.contrib.gis.db.models.manager import GeoManager

rules = [
     (
         (AutoSlugField, ),
         [],
         {
             "populate_from": ["_populate_from", {"default": "title"}],
         },
     ),
]
add_introspection_rules(rules, ["^django_extensions\.db\.fields"])

rules = [
     (
         (StdImageField, ),
         [],
         {
             "size": ["size", {"default": None}],
             "thumbnail_size": ["thumbnail_size", {"default": None}],
         },
     ),
]
add_introspection_rules(rules, ["^stdimage\.fields",])


class Station(LocativeModel):
    author = models.ForeignKey(User, related_name="authored_spotter_stations")
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    plot = models.ForeignKey(Plot, related_name="spotter_stations")
    time_limit = models.IntegerField(default=300)
    marker_icon = models.ImageField(null=True, blank=True, upload_to="img/spotter/stations/",
                                    verbose_name="Marker icon",
                                    help_text="This 72x72 pixel image will appear on the map screen. Please make it a PNG with transparency.")
    
    def __unicode__(self):
        return self.title

    def marker_icon_url(): #@NoSelf
        doc = """The url of the station's marker icon""" #@UnusedVariable
       
        def fget(self):
            try:
                return self.marker_icon.url
            except ValueError:
                return checkerboard.settings.MEDIA_URL + "img/spotter/missing_marker_icon.png"
           
        return locals()
       
    marker_icon_url = property(**marker_icon_url())
    

class Inquiry(TimeStampedModel):
    author = models.ForeignKey(User, related_name="authored_spotter_inquiries")
    station = models.ForeignKey(Station, related_name="inquiries")
    title = models.CharField(max_length=50)
    description = models.TextField("Short Description",null=True, blank=True)    
    long_description = models.TextField("Long Description",null=True, blank=True)    
    instructions = models.TextField("Instructions",null=True, blank=True)    
    payoff = models.TextField("Payoff",null=True, blank=True)    
    investigators = models.ManyToManyField(User, related_name="investigated_spotter_inquiries", through="Spotting")
    
    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Activities"
        ordering = ("created","title","station__title")
#        verbose_name_plural = "Inquiries"
#        verbose_name_plural = "Inquiries"

    def __unicode__(self):
        return "%s @ %s" % (self.title, self.station)


class SnapshotManager(GeoManager):
    def get_query_set(self):
        return super(SnapshotManager, self).get_query_set().filter(is_snapshot = True)

class Spotting(LocativeModel):
    image = StdImageField(upload_to='img/spotter/spottings/', null=True, blank=True, size=(480, 640), thumbnail_size=(48,64))
    inquiry = models.ForeignKey(Inquiry, null=True, blank=True, related_name="spottings")
    author = models.ForeignKey(User, related_name="spotter_spottings")
    taken_on = models.DateTimeField(null=True, blank=True)
    is_snapshot = models.BooleanField(default=False,
                                      verbose_name="Timeline snapshot?",
                                      help_text="Should this observation image be associated with the its activity timeline?")
    in_widget = models.BooleanField(default=True,
                                      verbose_name="Include in widgets?",
                                      help_text="Should this observation image be included in remote app widgets?")
    caption = models.CharField(max_length=300,null=True,blank=True)
   
 
    objects = GeoManager()
    snapshots = SnapshotManager()

    class Meta:
        verbose_name = "Observation"
        verbose_name_plural = "Observations"
        ordering = ("-modified","-taken_on")

    def image_url(): #@NoSelf
        doc = """The url of the spotting's image""" #@UnusedVariable
       
        def fget(self):
            try:
                return self.image.url
            except ValueError:
                return checkerboard.settings.MEDIA_URL + "img/spotter/missing_spotting.png"
           
        return locals()
       
    image_url = property(**image_url())
    
    def date(): #@NoSelf
        doc = """The date of the spotting""" #@UnusedVariable
       
        def fget(self):
            if self.taken_on is None:
                return self.created
            else:
                return self.taken_on
    
        return locals()

    date = property(**date())
    
    def answer_text(): #@NoSelf
        doc = """Retrives a textual version of the answers for this spotting""" #@UnusedVariable
       
        def fget(self):
            answers = []
            for answer in self.answers.all():
                text = "Q: %s\n" % answer.question.body

                try:
                    text += "A: %s\n" % getattr(answer,"textualanswer",None).body
                except:
                    pass
                
                try:
                    text += "A: %d\n" % getattr(answer,"numericanswer",None).value
                except:
                    pass
                
                try:
                    test = getattr(answer,"booleananswer",None).value
                    if test:
                        text += "A: true\n"
                    else:
                        text += "A: false\n"
                except answer.DoesNotExist:
                    pass
                
                if isinstance(answer,TextualAnswer.__class__):
                    text += "A: %s\n" % answer.body
                elif isinstance(answer,NumericAnswer.__class__):
                    text += "A: %d\n" % answer.value
                else:
                    try:
                        text += "A: %s\n" % answer.body
                    except:
                        pass
                    try:
                        text += "A: %d\n" % answer.value
                    except:
                        pass
                answers.append(text)
            return "\n".join(answers)
           
        return locals()
       
    answer_text = property(**answer_text())
    
    def __unicode__(self):
        return "%s by %s on %s" % (self.inquiry,self.author,self.created) 
    
    def save(self, *args, **kwargs):
        super(Spotting,self).save(*args, **kwargs)
        exists = Accomplishment.objects.filter(content_type__name="spotting",object_id=self.pk)
        if len(exists) == 0:
            Accomplishment.objects.create(content_object=self,user=self.author)
        else:
            exists[0].modified = datetime.datetime.now()


     
class CurrentManager(models.Manager):
    def get_query_set(self):
        return super(CurrentManager, self).get_query_set().filter(starting__lt = datetime.datetime.now(),
                                                                  ending__gt = datetime.datetime.now())

class Question(TimeStampedModel):
    body = models.TextField()
    order = models.IntegerField(default=10)
    inquiry = models.ForeignKey(Inquiry, related_name="questions")
    user = models.ForeignKey(User, related_name="spotter_questions")
    starting = models.DateTimeField(default = datetime.datetime.now())
    ending = models.DateTimeField(default = datetime.datetime.now() + datetime.timedelta(days=28))

    current = CurrentManager()
    objects = models.Manager()

    def __unicode__(self):
        return "%s: %s" % (self.inquiry,self.body[:50])
    
    class Meta:
        ordering = ("order",)

    def field_dict(): #@NoSelf
        doc = """Draws the field dict from the subclasses""" #@UnusedVariable
       
        def fget(self):
            try:
                q = self.numericquestion
            except Question.DoesNotExist:
                try:
                    q = self.textualquestion
                except Question.DoesNotExist:
                    try:
                        q = self.booleanquestion
                    except Question.DoesNotExist:
                            return None
                        
            return q.field_dict
           
        return locals()
       
    field_dict = property(**field_dict())
    
class NumericQuestion(Question):
    lower_bound = models.IntegerField(default=0)
    upper_bound = models.IntegerField(default=10)
    
    def field_dict(): #@NoSelf
        doc = """A dictionary that describes the question field""" #@UnusedVariable
       
        def fget(self):
            return {'type':'numeric','lower_bound':self.lower_bound,'upper_bound':self.upper_bound}
           
        return locals()
       
    field_dict = property(**field_dict())
    
class BooleanQuestion(Question):    
    true_text = models.CharField(max_length=30,default="true")
    false_text = models.CharField(max_length=30,default="false")

    def field_dict(): #@NoSelf
        doc = """A dictionary that describes the question field""" #@UnusedVariable
       
        def fget(self):
            return {'type':'boolean','true_text':self.true_text,'false_text':self.false_text}
           
        return locals()
       
    field_dict = property(**field_dict())
    
class TextualQuestion(Question):    

    def field_dict(): #@NoSelf
        doc = """A dictionary that describes the question field""" #@UnusedVariable
       
        def fget(self):
            return {'type':'textual',}
           
        return locals()
       
    field_dict = property(**field_dict())
    

class Answer(TimeStampedModel):
    question = models.ForeignKey(Question, related_name="answers")
    spotting = models.ForeignKey(Spotting, related_name="answers")
    
    def __unicode__(self):
        return "%s answers %s" % (self.spotting.author,self.question)
    
    def value_text(): #@NoSelf
        doc = """Returns the string representation of the answer's value or body""" #@UnusedVariable
       
        def fget(self):
            try:
                return unicode(self.numericanswer)
            except Answer.DoesNotExist:
                try:
                    return unicode(self.textualanswer)
                except Answer.DoesNotExist:
                    try:
                        return unicode(self.booleananswer)
                    except Answer.DoesNotExist:
                        return None
           
        return locals()
       
    value_text = property(**value_text())
    
    
class NumericAnswer(Answer):
    value = models.IntegerField(default=0)
    
    def __unicode__(self):
        return u"in %s, %s answered %s as %d" % (self.question.inquiry, self.spotting.author,self.question.body,self.value)    
    
    def save(self, *args, **kwargs):
        super(NumericAnswer,self).save(*args, **kwargs)
        exists = Accomplishment.objects.filter(content_type__name="numeric answer",object_id=self.pk)
        if len(exists) == 0:
            Accomplishment.objects.create(content_object=self,user=self.spotting.author)
        else:
            exists[0].modified = datetime.datetime.now()


class TextualAnswer(Answer):    
    body = models.TextField(null=True,blank=True)

    def __unicode__(self):
        if self.body:
            return u"in %s, %s answered %s as %s" % (self.question.inquiry, self.spotting.author,self.question.body,self.body)    
        else:
            return u"null"
    
    def save(self, *args, **kwargs):
        super(TextualAnswer,self).save(*args, **kwargs)
        exists = Accomplishment.objects.filter(content_type__name="textual answer",object_id=self.pk)
        if len(exists) == 0:
            Accomplishment.objects.create(content_object=self,user=self.spotting.author)
        else:
            exists[0].modified = datetime.datetime.now()

class BooleanAnswer(Answer):    
    value = models.NullBooleanField(blank=True)
    
    def __unicode__(self):
        if self.value:
            return u"in %s, %s answered %s as %s" % (self.question.inquiry, self.spotting.author,self.question.body,self.question.booleanquestion.true_text)    
        else:
            return u"in %s, %s answered %s as %s" % (self.question.inquiry, self.spotting.author,self.question.body,self.question.booleanquestion.false_text)    

    def save(self, *args, **kwargs):
        super(BooleanAnswer,self).save(*args, **kwargs)
        exists = Accomplishment.objects.filter(content_type__name="boolean answer",object_id=self.pk)
        if len(exists) == 0:
            Accomplishment.objects.create(content_object=self,user=self.spotting.author)
        else:
            exists[0].modified = datetime.datetime.now()

class Accomplishment(TimeStampedModel):
    user = models.ForeignKey(User, related_name="accomplishments")
    reviewers = models.ManyToManyField(User, related_name="reviewed_accomplishments", through="Review", blank="True")
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return "%s %s" % (self.user,unicode(self.content_object))
    
    def station(): #@NoSelf
        doc = """Returns the station""" #@UnusedVariable
       
        def fget(self):
            if self.content_object is not None:
                if self.content_type.name == "spotting":
                    return self.content_object.inquiry.station
                else:
                    return self.content_object.question.inquiry.station
            return None
           
        return locals()
       
    station = property(**station())

    def inquiry(): #@NoSelf
        doc = """Returns the inquiry""" #@UnusedVariable
       
        def fget(self):
            if self.content_type.name == "spotting":
                return self.content_object.inquiry
            else:
                return self.content_object.question.inquiry
           
        return locals()
       
    inquiry = property(**inquiry())
    
    def content(): #@NoSelf
        doc = """Return the specific content for the content_object""" #@UnusedVariable
       
        def fget(self):
            if self.content_type.name == "spotting":
                if self.content_object.image:
                    return {"image":self.content_object.image.url,"thumbnail":self.content_object.image.thumbnail.url()}
                else:
                    return {"image":None,"thumbnail":None}
            else:
                if self.content_type.name == "textual answer":
                    value = self.content_object.body
                else:
                    value = self.content_object.value
                return {"question":self.content_object.question.body,"answer":value}
           
        return locals()
       
    content = property(**content())

class Review(TimeStampedModel):
    accomplishment = models.ForeignKey(Accomplishment, related_name="reviews")
    reviewer = models.ForeignKey(User, related_name="reviews")
    notes = models.TextField(null=True,blank=True)

class Badge(TitleSlugDescriptionModel):
    users = models.ManyToManyField(User, related_name="badges", through="Win")
    accomplishments = models.ManyToManyField(Accomplishment, related_name="badges")
    image = StdImageField(upload_to='img/spotter/badges/', blank=True, size=(120, 120), thumbnail_size=(48,48))
    email_description = models.TextField(null=True,blank=True)
    
    def __unicode__(self):
        return self.title
    
class Win(TimeStampedModel):
    user = models.ForeignKey(User, related_name="wins")
    badge = models.ForeignKey(Badge, related_name="wins")
    complete = models.BooleanField(default=False)
    email_sent = models.BooleanField(default=False)
