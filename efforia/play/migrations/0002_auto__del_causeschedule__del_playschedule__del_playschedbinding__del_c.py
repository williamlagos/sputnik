# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'CauseSchedule'
        db.delete_table('play_causeschedule')

        # Deleting model 'PlaySchedule'
        db.delete_table('play_playschedule')

        # Deleting model 'PlaySchedBinding'
        db.delete_table('play_playschedbinding')

        # Deleting model 'CauseSchedBinding'
        db.delete_table('play_causeschedbinding')

        # Adding model 'MovementBinding'
        db.create_table('play_movementbinding', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cause', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['create.Causable'])),
            ('bind', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['create.Causable'])),
        ))
        db.send_create_signal('play', ['MovementBinding'])

        # Adding model 'Movement'
        db.create_table('play_movement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['auth.User'])),
            ('cause', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['create.Causable'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('play', ['Movement'])

        # Adding model 'Schedule'
        db.create_table('play_schedule', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['auth.User'])),
            ('play', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['play.Playable'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('play', ['Schedule'])

        # Adding model 'ScheduleBinding'
        db.create_table('play_schedulebinding', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('play', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['create.Causable'])),
            ('bind', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['create.Causable'])),
        ))
        db.send_create_signal('play', ['ScheduleBinding'])


    def backwards(self, orm):
        
        # Adding model 'CauseSchedule'
        db.create_table('play_causeschedule', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['auth.User'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('cause', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['create.Causable'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('play', ['CauseSchedule'])

        # Adding model 'PlaySchedule'
        db.create_table('play_playschedule', (
            ('play', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['play.Playable'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['auth.User'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('play', ['PlaySchedule'])

        # Adding model 'PlaySchedBinding'
        db.create_table('play_playschedbinding', (
            ('bind', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['create.Causable'])),
            ('play', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['create.Causable'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('play', ['PlaySchedBinding'])

        # Adding model 'CauseSchedBinding'
        db.create_table('play_causeschedbinding', (
            ('bind', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['create.Causable'])),
            ('cause', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['create.Causable'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('play', ['CauseSchedBinding'])

        # Deleting model 'MovementBinding'
        db.delete_table('play_movementbinding')

        # Deleting model 'Movement'
        db.delete_table('play_movement')

        # Deleting model 'Schedule'
        db.delete_table('play_schedule')

        # Deleting model 'ScheduleBinding'
        db.delete_table('play_schedulebinding')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
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
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'create.causable': {
            'Meta': {'object_name': 'Causable'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'video': ('django.db.models.fields.TextField', [], {})
        },
        'play.movement': {
            'Meta': {'object_name': 'Movement'},
            'cause': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['create.Causable']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['auth.User']"})
        },
        'play.movementbinding': {
            'Meta': {'object_name': 'MovementBinding'},
            'bind': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['create.Causable']"}),
            'cause': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['create.Causable']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'play.playable': {
            'Meta': {'object_name': 'Playable'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['auth.User']"})
        },
        'play.schedule': {
            'Meta': {'object_name': 'Schedule'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'play': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['play.Playable']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['auth.User']"})
        },
        'play.schedulebinding': {
            'Meta': {'object_name': 'ScheduleBinding'},
            'bind': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['create.Causable']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'play': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['create.Causable']"})
        }
    }

    complete_apps = ['play']
