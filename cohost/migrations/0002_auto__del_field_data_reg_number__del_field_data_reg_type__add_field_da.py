# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Data.reg_number'
        db.delete_column('Data', 'reg_number')

        # Deleting field 'Data.reg_type'
        db.delete_column('Data', 'reg_type')

        # Adding field 'Data.icpno'
        db.add_column('Data', 'icpno',
                      self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Data.organizers_type'
        db.add_column('Data', 'organizers_type',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Data.exadate'
        db.add_column('Data', 'exadate',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Data.reg_number'
        db.add_column('Data', 'reg_number',
                      self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Data.reg_type'
        db.add_column('Data', 'reg_type',
                      self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Data.icpno'
        db.delete_column('Data', 'icpno')

        # Deleting field 'Data.organizers_type'
        db.delete_column('Data', 'organizers_type')

        # Deleting field 'Data.exadate'
        db.delete_column('Data', 'exadate')


    models = {
        u'cohost.allkey': {
            'Meta': {'object_name': 'Allkey', 'db_table': "'AllKey'"},
            'bactive': ('django.db.models.fields.IntegerField', [], {'db_column': "'bActive'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128', 'db_column': "'KeyName'"}),
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
            'exadate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'icpno': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.TextField', [], {'db_column': "'IP'"}),
            'organizers_type': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '32', 'blank': 'True'}),
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