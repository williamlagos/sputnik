# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Event.user'
        db.delete_column(u'promote_event', 'user_id')

        # Deleting field 'Event.end_time'
        db.delete_column(u'promote_event', 'end_time')

        # Deleting field 'Event.name'
        db.delete_column(u'promote_event', 'name')

        # Deleting field 'Event.rsvp_status'
        db.delete_column(u'promote_event', 'rsvp_status')

        # Deleting field 'Event.date'
        db.delete_column(u'promote_event', 'date')

        # Deleting field 'Event.start_time'
        db.delete_column(u'promote_event', 'start_time')

        # Deleting field 'Event.id'
        db.delete_column(u'promote_event', u'id')

        # Deleting field 'Event.id_event'
        db.delete_column(u'promote_event', 'id_event')

        # Adding field 'Event.sellable_ptr'
        db.add_column(u'promote_event', u'sellable_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=1, to=orm['efforia.Sellable'], unique=True, primary_key=True),
                      keep_default=False)

        # Adding field 'Event.description'
        db.add_column(u'promote_event', 'description',
                      self.gf('django.db.models.fields.TextField')(default='', max_length=500),
                      keep_default=False)

        # Adding field 'Event.deadline'
        db.add_column(u'promote_event', 'deadline',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 5, 16, 0, 0)),
                      keep_default=False)

        # Adding field 'Event.max'
        db.add_column(u'promote_event', 'max',
                      self.gf('django.db.models.fields.IntegerField')(default=10),
                      keep_default=False)

        # Adding field 'Event.min'
        db.add_column(u'promote_event', 'min',
                      self.gf('django.db.models.fields.IntegerField')(default=2),
                      keep_default=False)


        # Changing field 'Event.location'
        db.alter_column(u'promote_event', 'location', self.gf('django.db.models.fields.CharField')(max_length=200))

    def backwards(self, orm):
        # Adding field 'Event.user'
        db.add_column(u'promote_event', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='+', to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Event.end_time'
        db.add_column(u'promote_event', 'end_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 5, 2, 0, 0)),
                      keep_default=False)

        # Adding field 'Event.name'
        db.add_column(u'promote_event', 'name',
                      self.gf('django.db.models.fields.CharField')(default='@@', max_length=50),
                      keep_default=False)

        # Adding field 'Event.rsvp_status'
        db.add_column(u'promote_event', 'rsvp_status',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=30),
                      keep_default=False)

        # Adding field 'Event.date'
        db.add_column(u'promote_event', 'date',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 5, 2, 0, 0), auto_now_add=True, blank=True),
                      keep_default=False)

        # Adding field 'Event.start_time'
        db.add_column(u'promote_event', 'start_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 5, 2, 0, 0)),
                      keep_default=False)

        # Adding field 'Event.id'
        db.add_column(u'promote_event', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=1, primary_key=True),
                      keep_default=False)

        # Adding field 'Event.id_event'
        db.add_column(u'promote_event', 'id_event',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=15),
                      keep_default=False)

        # Deleting field 'Event.sellable_ptr'
        db.delete_column(u'promote_event', u'sellable_ptr_id')

        # Deleting field 'Event.description'
        db.delete_column(u'promote_event', 'description')

        # Deleting field 'Event.deadline'
        db.delete_column(u'promote_event', 'deadline')

        # Deleting field 'Event.max'
        db.delete_column(u'promote_event', 'max')

        # Deleting field 'Event.min'
        db.delete_column(u'promote_event', 'min')


        # Changing field 'Event.location'
        db.alter_column(u'promote_event', 'location', self.gf('django.db.models.fields.CharField')(max_length=100))

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'efforia.sellable': {
            'Meta': {'object_name': 'Sellable'},
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 16, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'$$'", 'max_length': '150'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['auth.User']"}),
            'value': ('django.db.models.fields.FloatField', [], {'default': '1.0'})
        },
        u'promote.event': {
            'Meta': {'object_name': 'Event', '_ormbases': [u'efforia.Sellable']},
            'deadline': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 16, 0, 0)'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '500'}),
            'location': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'max': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'min': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            u'sellable_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['efforia.Sellable']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'promote.interest': {
            'Meta': {'object_name': 'Interest'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['promote.Project']"})
        },
        u'promote.movement': {
            'Meta': {'object_name': 'Movement'},
            'cause': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['promote.Project']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['auth.User']"})
        },
        u'promote.pledge': {
            'Meta': {'object_name': 'Pledge'},
            'backer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'backer'", 'to': u"orm['auth.User']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'$#'", 'max_length': '10'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project'", 'to': u"orm['promote.Project']"}),
            'value': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'promote.project': {
            'Meta': {'object_name': 'Project'},
            'content': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'credit': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 16, 0, 0)'}),
            'funded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 16, 0, 0)'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'visual': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'ytoken': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '15'})
        },
        u'promote.promoted': {
            'Meta': {'object_name': 'Promoted'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'@#'", 'max_length': '2'}),
            'prom': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['promote']