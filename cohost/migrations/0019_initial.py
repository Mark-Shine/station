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
            ('IPS', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(default='0', max_length=32, blank=True)),
            ('contact_name', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('icpno', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('organizers_type', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('exadate', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('organizers', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('cate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cohost.Cate'], null=True, blank=True)),
            ('area', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cohost.Area'], null=True, blank=True)),
            ('beizhu', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('related_law', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cohost.LawRecord'], null=True, blank=True)),
        ))
        db.send_create_signal(u'cohost', ['Data'])

        # Adding model 'Area'
        db.create_table(u'cohost_area', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
        ))
        db.send_create_signal(u'cohost', ['Area'])

        # Adding model 'Ippiece'
        db.create_table(u'cohost_ippiece', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('piece', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('area', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cohost.Area'], null=True, blank=True)),
        ))
        db.send_create_signal(u'cohost', ['Ippiece'])

        # Adding model 'DataActionRecord'
        db.create_table(u'cohost_dataactionrecord', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cohost.Data'], null=True, blank=True)),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=24, null=True, blank=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
        ))
        db.send_create_signal(u'cohost', ['DataActionRecord'])

        # Adding model 'Ips'
        db.create_table(u'cohost_ips', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True, blank=True)),
            ('area', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cohost.Area'], null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.CharField')(max_length=6, null=True, blank=True)),
        ))
        db.send_create_signal(u'cohost', ['Ips'])

        # Adding model 'LawRecord'
        db.create_table(u'cohost_lawrecord', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('law', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('detail', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'cohost', ['LawRecord'])


    def backwards(self, orm):
        # Deleting model 'Keywords'
        db.delete_table(u'cohost_keywords')

        # Deleting model 'Cate'
        db.delete_table(u'cohost_cate')

        # Deleting model 'Allkey'
        db.delete_table('AllKey')

        # Deleting model 'Data'
        db.delete_table('Data')

        # Deleting model 'Area'
        db.delete_table(u'cohost_area')

        # Deleting model 'Ippiece'
        db.delete_table(u'cohost_ippiece')

        # Deleting model 'DataActionRecord'
        db.delete_table(u'cohost_dataactionrecord')

        # Deleting model 'Ips'
        db.delete_table(u'cohost_ips')

        # Deleting model 'LawRecord'
        db.delete_table(u'cohost_lawrecord')


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
            'beizhu': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'cate': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cohost.Cate']", 'null': 'True', 'blank': 'True'}),
            'contact_name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'descript': ('django.db.models.fields.TextField', [], {'db_column': "'Descript'", 'blank': 'True'}),
            'exadate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'icpno': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.TextField', [], {'db_column': "'IP'"}),
            'organizers': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'organizers_type': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'related_law': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cohost.LawRecord']", 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '32', 'blank': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {'db_column': "'Title'", 'blank': 'True'}),
            'uri': ('django.db.models.fields.TextField', [], {'db_column': "'URI'"})
        },
        u'cohost.dataactionrecord': {
            'Meta': {'object_name': 'DataActionRecord'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '24', 'null': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cohost.Data']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'cohost.ippiece': {
            'Meta': {'object_name': 'Ippiece'},
            'area': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cohost.Area']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'piece': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        u'cohost.ips': {
            'Meta': {'object_name': 'Ips'},
            'active': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'area': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cohost.Area']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'})
        },
        u'cohost.keywords': {
            'Meta': {'object_name': 'Keywords'},
            'cate': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cohost.Cate']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kword': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'})
        },
        u'cohost.lawrecord': {
            'Meta': {'object_name': 'LawRecord'},
            'detail': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'law': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['cohost']