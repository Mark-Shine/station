# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Data.cate'
        db.add_column('Data', 'cate',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cohost.Cate'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Data.IPS'
        db.add_column('Data', 'IPS',
                      self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Data.reg_number'
        db.add_column('Data', 'reg_number',
                      self.gf('django.db.models.fields.IntegerField')(default=0, blank=True),
                      keep_default=False)

        # Adding field 'Data.reg_type'
        db.add_column('Data', 'reg_type',
                      self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Data.state'
        db.add_column('Data', 'state',
                      self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Data.contact_name'
        db.add_column('Data', 'contact_name',
                      self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Data.time'
        db.add_column('Data', 'time',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Data.cate'
        db.delete_column('Data', 'cate_id')

        # Deleting field 'Data.IPS'
        db.delete_column('Data', 'IPS')

        # Deleting field 'Data.reg_number'
        db.delete_column('Data', 'reg_number')

        # Deleting field 'Data.reg_type'
        db.delete_column('Data', 'reg_type')

        # Deleting field 'Data.state'
        db.delete_column('Data', 'state')

        # Deleting field 'Data.contact_name'
        db.delete_column('Data', 'contact_name')

        # Deleting field 'Data.time'
        db.delete_column('Data', 'time')


    models = {
        u'cohost.allkey': {
            'Meta': {'object_name': 'Allkey', 'db_table': "'AllKey'"},
            'bactive': ('django.db.models.fields.IntegerField', [], {'db_column': "'bActive'"}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'ID'"}),
            'keyname': ('django.db.models.fields.TextField', [], {'unique': 'True', 'db_column': "'KeyName'"}),
            'usecount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'UseCount'", 'blank': 'True'}),
            'visitmonth': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'VisitMonth'", 'blank': 'True'})
        },
        u'cohost.cate': {
            'Meta': {'object_name': 'Cate'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        u'cohost.data': {
            'IPS': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'Meta': {'object_name': 'Data', 'db_table': "'Data'"},
            'cate': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cohost.Cate']", 'null': 'True', 'blank': 'True'}),
            'contact_name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'descript': ('django.db.models.fields.TextField', [], {'db_column': "'Descript'", 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'ID'"}),
            'ip': ('django.db.models.fields.TextField', [], {'db_column': "'IP'"}),
            'reg_number': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'reg_type': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {'db_column': "'Title'", 'blank': 'True'}),
            'uri': ('django.db.models.fields.TextField', [], {'db_column': "'URI'"})
        },
        u'cohost.keywords': {
            'Meta': {'object_name': 'Keywords'},
            'cate': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cohost.Cate']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kword': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['cohost']