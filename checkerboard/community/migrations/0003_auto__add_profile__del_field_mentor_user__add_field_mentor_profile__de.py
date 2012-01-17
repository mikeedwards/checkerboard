# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Profile'
        db.create_table('community_profile', (
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('modified', self.gf('django_extensions.db.fields.ModificationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('created', self.gf('django_extensions.db.fields.CreationDateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal('community', ['Profile'])

        # Deleting field 'Mentor.user'
        db.delete_column('community_mentor', 'user_id')

        # Adding field 'Mentor.profile'
        db.add_column('community_mentor', 'profile', self.gf('django.db.models.fields.related.OneToOneField')(default=1, related_name='mentor', unique=True, blank=True, to=orm['community.Profile']), keep_default=False)

        # Deleting field 'Learner.user'
        db.delete_column('community_learner', 'user_id')

        # Adding field 'Learner.profile'
        db.add_column('community_learner', 'profile', self.gf('django.db.models.fields.related.OneToOneField')(default=1, related_name='learner', unique=True, blank=True, to=orm['community.Profile']), keep_default=False)
    
    
    def backwards(self, orm):
        
        # Deleting model 'Profile'
        db.delete_table('community_profile')

        # Adding field 'Mentor.user'
        db.add_column('community_mentor', 'user', self.gf('django.db.models.fields.related.OneToOneField')(default=1, related_name='mentor', unique=True, to=orm['auth.User'], blank=True), keep_default=False)

        # Deleting field 'Mentor.profile'
        db.delete_column('community_mentor', 'profile_id')

        # Adding field 'Learner.user'
        db.add_column('community_learner', 'user', self.gf('django.db.models.fields.related.OneToOneField')(default=1, related_name='learner', unique=True, to=orm['auth.User'], blank=True), keep_default=False)

        # Deleting field 'Learner.profile'
        db.delete_column('community_learner', 'profile_id')
    
    
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
            'profile': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'learner'", 'unique': 'True', 'blank': 'True', 'to': "orm['community.Profile']"})
        },
        'community.mentor': {
            'Meta': {'object_name': 'Mentor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'profile': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'mentor'", 'unique': 'True', 'blank': 'True', 'to': "orm['community.Profile']"})
        },
        'community.profile': {
            'Meta': {'object_name': 'Profile'},
            'created': ('django_extensions.db.fields.CreationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django_extensions.db.fields.ModificationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }
    
    complete_apps = ['community']
