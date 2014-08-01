# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Keywords'
        db.create_table(u'cohost_keywords', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('kword', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('cate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cohost.Cate'], null=True, blank=True)),
        ))
        db.send_create_signal(u'cohost', ['Keywords'])

        # Adding model 'Cate'
        db.create_table(u'cohost_cate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
        ))
        db.send_create_signal(u'cohost', ['Cate'])

        # Adding model 'Allkey'
        db.create_table('AllKey', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bactive', self.gf('django.db.models.fields.IntegerField')(db_column='bActive')),
            ('keyname', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128, db_column='KeyName')),
            ('visitmonth', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='VisitMonth', blank=True)),
            ('usecount', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='UseCount', blank=True)),
        ))
        db.send_create_signal(u'cohost', ['Allkey'])

        # Adding model 'Data'
        db.create_table('Data', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip', self.gf('django.db.models.fields.TextField')(db_column='IP')),
            ('uri', self.gf('django.db.models.fields.TextField')(db_column='URI')),
            ('title', self.gf('django.db.models.fields.TextField')(db_column='Title', blank=True)),
            ('descript', self.gf('django.db.models.fields.TextField')(db_column='Descript', blank=True)),
            ('cate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cohost.Cate'], null=True, blank=True)),
            ('IPS', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('reg_number', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('reg_type', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(default='0', max_length=32, blank=True)),
            ('contact_name', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'cohost', ['Data'])


    def backwards(self, orm):
        # Deleting model 'Keywords'
        db.delete_table(u'cohost_keywords')

        # Deleting model 'Cate'
        db.delete_table(u'cohost_cate')

        # Deleting model 'Allkey'
        db.delete_table('AllKey')

        # Deleting model 'Data'
        db.delete_table('Data')


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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.TextField', [], {'db_column': "'IP'"}),
            'reg_number': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'reg_type': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
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