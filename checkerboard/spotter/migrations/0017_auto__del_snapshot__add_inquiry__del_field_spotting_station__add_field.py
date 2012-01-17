# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from checkerboard.spotter.models import Inquiry, Station
from django.contrib.auth.models import User

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Deleting model 'Snapshot'
        db.delete_table('spotter_snapshot')

        # Adding model 'Inquiry'
        db.create_table('spotter_inquiry', (
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='authored_spotter_inquiries', to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('modified', self.gf('django_extensions.db.fields.ModificationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('created', self.gf('django_extensions.db.fields.CreationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('station', self.gf('django.db.models.fields.related.ForeignKey')(related_name='inquiries', to=orm['spotter.Station'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('spotter', ['Inquiry'])

        # Deleting field 'Spotting.station'
        db.delete_column('spotter_spotting', 'station_id')

        # Adding field 'Spotting.taken_on'
        db.add_column('spotter_spotting', 'taken_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True), keep_default=False)

        # Adding field 'Spotting.inquiry'
        db.add_column('spotter_spotting', 'inquiry', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='spottings', null=True, to=orm['spotter.Inquiry']), keep_default=False)

        # Deleting field 'Question.station'
        db.delete_column('spotter_question', 'station_id')

        Inquiry.objects.create(station=Station.objects.all()[0],
                               author=User.objects.all()[0],
                               title="dummy",
                               description="dummy")

        # Adding field 'Question.inquiry'
        db.add_column('spotter_question', 'inquiry', self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='questions', to=orm['spotter.Inquiry']), keep_default=False)
    
    
    def backwards(self, orm):
        
        # Adding model 'Snapshot'
        db.create_table('spotter_snapshot', (
            ('taken_on', self.gf('django.db.models.fields.DateTimeField')()),
            ('created', self.gf('django_extensions.db.fields.CreationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='spotter_snapshots', to=orm['auth.User'])),
            ('modified', self.gf('django_extensions.db.fields.ModificationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('station', self.gf('django.db.models.fields.related.ForeignKey')(related_name='snapshots', to=orm['spotter.Station'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('spotter', ['Snapshot'])

        # Deleting model 'Inquiry'
        db.delete_table('spotter_inquiry')

        # Adding field 'Spotting.station'
        db.add_column('spotter_spotting', 'station', self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='spottings', to=orm['spotter.Station']), keep_default=False)

        # Deleting field 'Spotting.taken_on'
        db.delete_column('spotter_spotting', 'taken_on')

        # Deleting field 'Spotting.inquiry'
        db.delete_column('spotter_spotting', 'inquiry_id')

        # Adding field 'Question.station'
        db.add_column('spotter_question', 'station', self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='questions', to=orm['spotter.Station']), keep_default=False)

        # Deleting field 'Question.inquiry'
        db.delete_column('spotter_question', 'inquiry_id')
    
    
    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'community.plot': {
            'Meta': {'object_name': 'Plot'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'authored_plots'", 'to': "orm['auth.User']"}),
            'created': ('django_extensions.db.fields.CreationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django_extensions.db.fields.ModificationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'polygon': ('django.contrib.gis.db.models.fields.PolygonField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'spotter.answer': {
            'Meta': {'object_name': 'Answer'},
            'created': ('django_extensions.db.fields.CreationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django_extensions.db.fields.ModificationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answers'", 'to': "orm['spotter.Question']"}),
            'spotting': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answers'", 'to': "orm['spotter.Spotting']"})
        },
        'spotter.booleananswer': {
            'Meta': {'object_name': 'BooleanAnswer', '_ormbases': ['spotter.Answer']},
            'answer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['spotter.Answer']", 'unique': 'True', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'})
        },
        'spotter.booleanquestion': {
            'Meta': {'object_name': 'BooleanQuestion', '_ormbases': ['spotter.Question']},
            'false_text': ('django.db.models.fields.CharField', [], {'default': "'false'", 'max_length': '30'}),
            'question_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['spotter.Question']", 'unique': 'True', 'primary_key': 'True'}),
            'true_text': ('django.db.models.fields.CharField', [], {'default': "'true'", 'max_length': '30'})
        },
        'spotter.inquiry': {
            'Meta': {'object_name': 'Inquiry'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'authored_spotter_inquiries'", 'to': "orm['auth.User']"}),
            'created': ('django_extensions.db.fields.CreationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'investigators': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'investigated_spotter_inquiries'", 'symmetrical': 'False', 'through': "orm['spotter.Spotting']", 'to': "orm['auth.User']"}),
            'modified': ('django_extensions.db.fields.ModificationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'station': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'inquiries'", 'to': "orm['spotter.Station']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'spotter.numericanswer': {
            'Meta': {'object_name': 'NumericAnswer', '_ormbases': ['spotter.Answer']},
            'answer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['spotter.Answer']", 'unique': 'True', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'spotter.numericquestion': {
            'Meta': {'object_name': 'NumericQuestion', '_ormbases': ['spotter.Question']},
            'lower_bound': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'question_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['spotter.Question']", 'unique': 'True', 'primary_key': 'True'}),
            'upper_bound': ('django.db.models.fields.IntegerField', [], {'default': '10'})
        },
        'spotter.question': {
            'Meta': {'object_name': 'Question'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'created': ('django_extensions.db.fields.CreationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'ending': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 7, 29, 8, 47, 28, 685693)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inquiry': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questions'", 'to': "orm['spotter.Inquiry']"}),
            'modified': ('django_extensions.db.fields.ModificationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'starting': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 7, 1, 8, 47, 28, 685656)'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'spotter_questions'", 'to': "orm['auth.User']"})
        },
        'spotter.spotting': {
            'Meta': {'object_name': 'Spotting'},
            'accuracy': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'altitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'altitude_accuracy': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'spotter_spottings'", 'to': "orm['auth.User']"}),
            'created': ('django_extensions.db.fields.CreationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'inquiry': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'spottings'", 'null': 'True', 'to': "orm['spotter.Inquiry']"}),
            'modified': ('django_extensions.db.fields.ModificationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'taken_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'spotter.station': {
            'Meta': {'object_name': 'Station'},
            'accuracy': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'altitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'altitude_accuracy': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'authored_spotter_stations'", 'to': "orm['auth.User']"}),
            'created': ('django_extensions.db.fields.CreationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django_extensions.db.fields.ModificationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'plot': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'spotter_stations'", 'to': "orm['community.Plot']"}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'time_limit': ('django.db.models.fields.IntegerField', [], {'default': '300'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'spotter.textualanswer': {
            'Meta': {'object_name': 'TextualAnswer', '_ormbases': ['spotter.Answer']},
            'answer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['spotter.Answer']", 'unique': 'True', 'primary_key': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'spotter.textualquestion': {
            'Meta': {'object_name': 'TextualQuestion', '_ormbases': ['spotter.Question']},
            'question_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['spotter.Question']", 'unique': 'True', 'primary_key': 'True'})
        }
    }
    
    complete_apps = ['spotter']
