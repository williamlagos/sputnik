# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Product.user'
        db.delete_column('store_product', 'user_id')

        # Adding field 'Product.seller'
        db.add_column('store_product', 'seller', self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='+', to=orm['auth.User']), keep_default=False)

        # Deleting field 'Deliverable.email_receiver'
        db.delete_column('store_deliverable', 'email_receiver')

        # Adding field 'Deliverable.buyer'
        db.add_column('store_deliverable', 'buyer', self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='+', to=orm['auth.User']), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'Product.user'
        db.add_column('store_product', 'user', self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='+', to=orm['auth.User']), keep_default=False)

        # Deleting field 'Product.seller'
        db.delete_column('store_product', 'seller_id')

        # Adding field 'Deliverable.email_receiver'
        db.add_column('store_deliverable', 'email_receiver', self.gf('django.db.models.fields.CharField')(default='', max_length=50), keep_default=False)

        # Deleting field 'Deliverable.buyer'
        db.delete_column('store_deliverable', 'buyer_id')


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
        'store.deliverable': {
            'Meta': {'object_name': 'Deliverable'},
            'buyer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['auth.User']"}),
            'code': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'height': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'mail_code': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['store.Product']"}),
            'receiver': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'value': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'weight': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'width': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'store.product': {
            'Meta': {'object_name': 'Product'},
            'category': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'credit': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.date(2012, 6, 14)', 'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150'}),
            'seller': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['auth.User']"}),
            'visual': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40'})
        }
    }

    complete_apps = ['store']
