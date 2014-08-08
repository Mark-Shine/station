# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Area'
        db.create_table(u'cohost_area', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
        ))
        db.send_create_signal(u'cohost', ['Area'])

        # Adding field 'Data.area'
        db.add_column('Data', 'area',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cohost.Area'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Area'
        db.delete_table(u'cohost_area')

        # Deleting field 'Data.area'
        db.delete_column('Data', 'area_id')


    models = {
        u'cohost.allkey': {
            'Meta': {'object_name': 'Allkey', 'db_table': "'AllKey'"},
            'bactive': ('django.db.models.fields.IntegerField', [], {'db_column': "'bActive'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128', 'db_column': "'KeyName'"}),
            'usecount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'UseCount'", 'blank': 'True'}),
            'visitmonth': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'VisitMonth'", 'blank': 'True'})
        },
        u'cohost.area': {
            'Meta': {'object_name': 'Area'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        u'cohost.cate': {
            'Meta': {'object_name': 'Cate'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        u'cohost.data': {
            'IPS': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'Meta': {'object_name': 'Data', 'db_table': "'Data'"},
            'area': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cohost.Area']", 'null': 'True', 'blank': 'True'}),
            'cate': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cohost.Cate']", 'null': 'True', 'blank': 'True'}),
            'contact_name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'descript': ('django.db.models.fields.TextField', [], {'db_column': "'Descript'", 'blank': 'True'}),
            'exadate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'icpno': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.TextField', [], {'db_column': "'IP'"}),
            'organizers': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
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