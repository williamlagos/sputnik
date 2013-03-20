# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Promoted'
        db.create_table('promote_promoted', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='@#', max_length=2)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['auth.User'])),
            ('prom', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('promote', ['Promoted'])

        # Adding model 'Project'
        db.create_table('promote_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 3, 20, 0, 0))),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 3, 20, 0, 0))),
            ('content', self.gf('django.db.models.fields.TextField')(default='')),
            ('credit', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('ytoken', self.gf('django.db.models.fields.CharField')(default='', max_length=15)),
            ('visual', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('funded', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('promote', ['Project'])

        # Adding model 'Interest'
        db.create_table('promote_interest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(default='', max_length=25)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['promote.Project'])),
        ))
        db.send_create_signal('promote', ['Interest'])

        # Adding model 'Movement'
        db.create_table('promote_movement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['auth.User'])),
            ('cause', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['promote.Project'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('promote', ['Movement'])

        # Adding model 'Pledge'
        db.create_table('promote_pledge', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='$#', max_length=10)),
            ('value', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('backer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='backer', to=orm['auth.User'])),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='project', to=orm['promote.Project'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('promote', ['Pledge'])


    def backwards(self, orm):
        # Deleting model 'Promoted'
        db.delete_table('promote_promoted')

        # Deleting model 'Project'
        db.delete_table('promote_project')

        # Deleting model 'Interest'
        db.delete_table('promote_interest')

        # Deleting model 'Movement'
        db.delete_table('promote_movement')

        # Deleting model 'Pledge'
        db.delete_table('promote_pledge')


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
        'promote.interest': {
            'Meta': {'object_name': 'Interest'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['promote.Project']"})
        },
        'promote.movement': {
            'Meta': {'object_name': 'Movement'},
            'cause': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['promote.Project']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['auth.User']"})
        },
        'promote.pledge': {
            'Meta': {'object_name': 'Pledge'},
            'backer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'backer'", 'to': "orm['auth.User']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'$#'", 'max_length': '10'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project'", 'to': "orm['promote.Project']"}),
            'value': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'promote.project': {
            'Meta': {'object_name': 'Project'},
            'content': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'credit': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 3, 20, 0, 0)'}),
            'funded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 3, 20, 0, 0)'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'visual': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'ytoken': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '15'})
        },
        'promote.promoted': {
            'Meta': {'object_name': 'Promoted'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'@#'", 'max_length': '2'}),
            'prom': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['promote']