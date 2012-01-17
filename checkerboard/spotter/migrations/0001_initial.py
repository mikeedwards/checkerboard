# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Spotting'
        db.create_table('spotter_spotting', (
            ('created', self.gf('django_extensions.db.fields.CreationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('altitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('lon', self.gf('django.db.models.fields.FloatField')()),
            ('modified', self.gf('django_extensions.db.fields.ModificationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('altitude_accuracy', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('lat', self.gf('django.db.models.fields.FloatField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('accuracy', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal('spotter', ['Spotting'])

        # Adding model 'Question'
        db.create_table('spotter_question', (
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('created', self.gf('django_extensions.db.fields.CreationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django_extensions.db.fields.ModificationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('spotting', self.gf('django.db.models.fields.related.ForeignKey')(related_name='questions', to=orm['spotter.Spotting'])),
            ('mentor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='questions', to=orm['community.Mentor'])),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=10)),
        ))
        db.send_create_signal('spotter', ['Question'])

        # Adding model 'NumericQuestion'
        db.create_table('spotter_numericquestion', (
            ('lower_bound', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('question_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['spotter.Question'], unique=True, primary_key=True)),
            ('upper_bound', self.gf('django.db.models.fields.IntegerField')(default=10)),
        ))
        db.send_create_signal('spotter', ['NumericQuestion'])

        # Adding model 'TextualQuestion'
        db.create_table('spotter_textualquestion', (
            ('question_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['spotter.Question'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('spotter', ['TextualQuestion'])

        # Adding model 'Answer'
        db.create_table('spotter_answer', (
            ('learner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='answers', to=orm['community.Learner'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(related_name='answers', to=orm['spotter.Question'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('modified', self.gf('django_extensions.db.fields.ModificationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('created', self.gf('django_extensions.db.fields.CreationDateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal('spotter', ['Answer'])

        # Adding model 'NumericAnswer'
        db.create_table('spotter_numericanswer', (
            ('answer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['spotter.Answer'], unique=True, primary_key=True)),
            ('value', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('spotter', ['NumericAnswer'])

        # Adding model 'TextualAnswer'
        db.create_table('spotter_textualanswer', (
            ('body', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('answer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['spotter.Answer'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('spotter', ['TextualAnswer'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Spotting'
        db.delete_table('spotter_spotting')

        # Deleting model 'Question'
        db.delete_table('spotter_question')

        # Deleting model 'NumericQuestion'
        db.delete_table('spotter_numericquestion')

        # Deleting model 'TextualQuestion'
        db.delete_table('spotter_textualquestion')

        # Deleting model 'Answer'
        db.delete_table('spotter_answer')

        # Deleting model 'NumericAnswer'
        db.delete_table('spotter_numericanswer')

        # Deleting model 'TextualAnswer'
        db.delete_table('spotter_textualanswer')
    
    
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
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'learner'", 'unique': 'True', 'blank': 'True', 'to': "orm['auth.User']"})
        },
        'community.mentor': {
            'Meta': {'object_name': 'Mentor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mentor'", 'unique': 'True', 'blank': 'True', 'to': "orm['auth.User']"})
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
            'learner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answers'", 'to': "orm['community.Learner']"}),
            'modified': ('django_extensions.db.fields.ModificationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answers'", 'to': "orm['spotter.Question']"})
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mentor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questions'", 'to': "orm['community.Mentor']"}),
            'modified': ('django_extensions.db.fields.ModificationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'spotting': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questions'", 'to': "orm['spotter.Spotting']"})
        },
        'spotter.spotting': {
            'Meta': {'object_name': 'Spotting'},
            'accuracy': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'altitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'altitude_accuracy': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django_extensions.db.fields.CreationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lon': ('django.db.models.fields.FloatField', [], {}),
            'modified': ('django_extensions.db.fields.ModificationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
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
