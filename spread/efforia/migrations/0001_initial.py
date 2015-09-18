# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Profile'
        db.create_table(u'efforia_profile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('coins', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('visual', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('career', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('birthday', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 5, 14, 0, 0))),
            ('google_token', self.gf('django.db.models.fields.TextField')(default='', max_length=120)),
            ('twitter_token', self.gf('django.db.models.fields.TextField')(default='', max_length=120)),
            ('facebook_token', self.gf('django.db.models.fields.TextField')(default='', max_length=120)),
            ('bio', self.gf('django.db.models.fields.TextField')(default='', max_length=140)),
            ('interface', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('typeditor', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('monetize', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('language', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 5, 14, 0, 0), auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'efforia', ['Profile'])

        # Adding model 'Place'
        db.create_table(u'efforia_place', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('code', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('city', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('country', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 5, 14, 0, 0), auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'efforia', ['Place'])

        # Adding model 'Followed'
        db.create_table(u'efforia_followed', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('followed', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('follower', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'efforia', ['Followed'])

        # Adding model 'Page'
        db.create_table(u'efforia_page', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='!#', max_length=50)),
            ('content', self.gf('django.db.models.fields.TextField')(default='')),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['auth.User'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'efforia', ['Page'])

        # Adding model 'Basket'
        db.create_table(u'efforia_basket', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='++', max_length=2)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['auth.User'])),
            ('deliverable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('product', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('quantity', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'efforia', ['Basket'])

        # Adding model 'Sellable'
        db.create_table(u'efforia_sellable', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='$$', max_length=150)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['auth.User'])),
            ('value', self.gf('django.db.models.fields.FloatField')(default=1.0)),
        ))
        db.send_create_signal(u'efforia', ['Sellable'])

        # Adding model 'Deliverable'
        db.create_table(u'efforia_deliverable', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='((', max_length=50)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['auth.User'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['efforia.Sellable'])),
            ('mail_code', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('height', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('length', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('width', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('weight', self.gf('django.db.models.fields.IntegerField')(default=10)),
            ('value', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 5, 14, 0, 0), auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'efforia', ['Deliverable'])


    def backwards(self, orm):
        # Deleting model 'Profile'
        db.delete_table(u'efforia_profile')

        # Deleting model 'Place'
        db.delete_table(u'efforia_place')

        # Deleting model 'Followed'
        db.delete_table(u'efforia_followed')

        # Deleting model 'Page'
        db.delete_table(u'efforia_page')

        # Deleting model 'Basket'
        db.delete_table(u'efforia_basket')

        # Deleting model 'Sellable'
        db.delete_table(u'efforia_sellable')

        # Deleting model 'Deliverable'
        db.delete_table(u'efforia_deliverable')


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
        u'efforia.basket': {
            'Meta': {'object_name': 'Basket'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deliverable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'++'", 'max_length': '2'}),
            'product': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['auth.User']"})
        },
        u'efforia.deliverable': {
            'Meta': {'object_name': 'Deliverable'},
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 14, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'mail_code': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'(('", 'max_length': '50'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['efforia.Sellable']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['auth.User']"}),
            'value': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'weight': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'width': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'efforia.followed': {
            'Meta': {'object_name': 'Followed'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'followed': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'follower': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'efforia.page': {
            'Meta': {'object_name': 'Page'},
            'content': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'!#'", 'max_length': '50'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['auth.User']"})
        },
        u'efforia.place': {
            'Meta': {'object_name': 'Place'},
            'city': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'code': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 14, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'efforia.profile': {
            'Meta': {'object_name': 'Profile'},
            'bio': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '140'}),
            'birthday': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 14, 0, 0)'}),
            'career': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'coins': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 14, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'facebook_token': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '120'}),
            'google_token': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '120'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interface': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'language': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'monetize': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'twitter_token': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '120'}),
            'typeditor': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'visual': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'})
        },
        u'efforia.sellable': {
            'Meta': {'object_name': 'Sellable'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'$$'", 'max_length': '150'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['auth.User']"}),
            'value': ('django.db.models.fields.FloatField', [], {'default': '1.0'})
        }
    }

    complete_apps = ['efforia']