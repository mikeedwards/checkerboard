# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding field 'Extent.polygon'
        db.add_column('spotter_extent', 'polygon', self.gf('django.contrib.gis.db.models.fields.PolygonField')(default=None), keep_default=False)
    
    
    def backwards(self, orm):
        
        # Deleting field 'Extent.polygon'
        db.delete_column('spotter_extent', 'polygon')
    
    
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
        'community.learner': {
            'Meta': {'object_name': 'Learner'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'learner'", 'unique': 'True', 'blank': 'True', 'to': "orm['auth.User']"})
        },
        'community.mentor': {
            'Meta': {'object_name': 'Mentor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'mentor'", 'unique': 'True', 'blank': 'True', 'to': "orm['auth.User']"})
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
        'spotter.extent': {
            'Meta': {'object_name': 'Extent'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'authored_extents'", 'to': "orm['community.Mentor']"}),
            'created': ('django_extensions.db.fields.CreationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'geodetic_system': ('django.db.models.fields.CharField', [], {'default': "'WGS 84'", 'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat_ne': ('django.db.models.fields.FloatField', [], {}),
            'lat_sw': ('django.db.models.fields.FloatField', [], {}),
            'lon_ne': ('django.db.models.fields.FloatField', [], {}),
            'lon_sw': ('django.db.models.fields.FloatField', [], {}),
            'modified': ('django_extensions.db.fields.ModificationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'polygon': ('django.contrib.gis.db.models.fields.PolygonField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'spotter.habitat': {
            'Meta': {'object_name': 'Habitat'},
            'accuracy': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'altitude_accuracy': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'authored_habitats'", 'to': "orm['community.Mentor']"}),
            'created': ('django_extensions.db.fields.CreationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'extent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'habitats'", 'to': "orm['spotter.Extent']"}),
            'geodetic_system': ('django.db.models.fields.CharField', [], {'default': "'WGS 84'", 'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'investigators': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'investigated_habitats'", 'symmetrical': 'False', 'through': "orm['spotter.Spotting']", 'to': "orm['community.Learner']"}),
            'modified': ('django_extensions.db.fields.ModificationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {}),
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
            'habitat': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questions'", 'to': "orm['spotter.Habitat']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mentor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questions'", 'to': "orm['community.Mentor']"}),
            'modified': ('django_extensions.db.fields.ModificationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '10'})
        },
        'spotter.spotting': {
            'Meta': {'object_name': 'Spotting'},
            'accuracy': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'altitude_accuracy': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'spottings'", 'to': "orm['community.Learner']"}),
            'created': ('django_extensions.db.fields.CreationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'geodetic_system': ('django.db.models.fields.CharField', [], {'default': "'WGS 84'", 'max_length': '50'}),
            'habitat': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'spottings'", 'to': "orm['spotter.Habitat']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'modified': ('django_extensions.db.fields.ModificationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {})
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
