# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Badge'
        db.create_table('spotter_badge', (
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('slug', self.gf('django_extensions.db.fields.AutoSlugField')(db_index=True, max_length=50, blank=True, populate_from='title')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('thumbnail', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('spotter', ['Badge'])

        # Adding M2M table for field accomplishments on 'Badge'
        db.create_table('spotter_badge_accomplishments', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('badge', models.ForeignKey(orm['spotter.badge'], null=False)),
            ('accomplishment', models.ForeignKey(orm['spotter.accomplishment'], null=False))
        ))
        db.create_unique('spotter_badge_accomplishments', ['badge_id', 'accomplishment_id'])

        # Adding model 'Win'
        db.create_table('spotter_win', (
            ('complete', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('created', self.gf('django_extensions.db.fields.CreationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django_extensions.db.fields.ModificationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='wins', to=orm['auth.User'])),
            ('badge', self.gf('django.db.models.fields.related.ForeignKey')(related_name='wins', to=orm['spotter.Badge'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('spotter', ['Win'])

        # Adding model 'Accomplishment'
        db.create_table('spotter_accomplishment', (
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('created', self.gf('django_extensions.db.fields.CreationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('modified', self.gf('django_extensions.db.fields.ModificationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='accomplishments', to=orm['auth.User'])),
            ('reviewed_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('reviewer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='accomplishments_reviewed', null='True', to=orm['auth.User'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('spotter', ['Accomplishment'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Badge'
        db.delete_table('spotter_badge')

        # Removing M2M table for field accomplishments on 'Badge'
        db.delete_table('spotter_badge_accomplishments')

        # Deleting model 'Win'
        db.delete_table('spotter_win')

        # Deleting model 'Accomplishment'
        db.delete_table('spotter_accomplishment')
    
    
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
        'spotter.accomplishment': {
            'Meta': {'object_name': 'Accomplishment'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created': ('django_extensions.db.fields.CreationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django_extensions.db.fields.ModificationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'reviewed_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'reviewer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'accomplishments_reviewed'", 'null': "'True'", 'to': "orm['auth.User']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'accomplishments'", 'to': "orm['auth.User']"})
        },
        'spotter.answer': {
            'Meta': {'object_name': 'Answer'},
            'created': ('django_extensions.db.fields.CreationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django_extensions.db.fields.ModificationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answers'", 'to': "orm['spotter.Question']"}),
            'spotting': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answers'", 'to': "orm['spotter.Spotting']"})
        },
        'spotter.badge': {
            'Meta': {'object_name': 'Badge'},
            'accomplishments': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'badges'", 'symmetrical': 'False', 'to': "orm['spotter.Accomplishment']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True', 'populate_from': "'title'"}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'badges'", 'symmetrical': 'False', 'through': "orm['spotter.Win']", 'to': "orm['auth.User']"})
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
            'ending': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 8, 12, 12, 22, 30, 76482)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inquiry': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questions'", 'to': "orm['spotter.Inquiry']"}),
            'modified': ('django_extensions.db.fields.ModificationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'starting': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 7, 15, 12, 22, 30, 76450)'}),
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
            'is_snapshot': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
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
        },
        'spotter.win': {
            'Meta': {'object_name': 'Win'},
            'badge': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wins'", 'to': "orm['spotter.Badge']"}),
            'complete': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'created': ('django_extensions.db.fields.CreationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django_extensions.db.fields.ModificationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wins'", 'to': "orm['auth.User']"})
        }
    }
    
    complete_apps = ['spotter']
