# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Store.inventory'
        db.delete_column(u'bookservices_store', 'inventory_id')

        # Adding field 'Inventory.store'
        db.add_column(u'bookservices_inventory', 'store',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['bookservices.Store']),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Store.inventory'
        db.add_column(u'bookservices_store', 'inventory',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['bookservices.Inventory']),
                      keep_default=False)

        # Deleting field 'Inventory.store'
        db.delete_column(u'bookservices_inventory', 'store_id')


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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'bookservices.inventory': {
            'Meta': {'object_name': 'Inventory'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bookservices.LibraryBook']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bookservices.Store']"})
        },
        u'bookservices.librarybook': {
            'Meta': {'object_name': 'LibraryBook'},
            'author': ('django.db.models.fields.TextField', [], {'max_length': '1000'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'blank': 'True'}),
            'genre': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'isbn_10': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'isbn_13': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '13', 'primary_key': 'True', 'db_index': 'True'}),
            'publish_date': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'publisher': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250', 'db_index': 'True'})
        },
        u'bookservices.store': {
            'Meta': {'object_name': 'Store'},
            'allowedUsers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'store'", 'symmetrical': 'False', 'through': u"orm['bookservices.UserToStore']", 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'bookservices.usertostore': {
            'Meta': {'object_name': 'UserToStore'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'permission': ('django.db.models.fields.CharField', [], {'default': "'rw'", 'max_length': '15'}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bookservices.Store']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['bookservices']