# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'EventInfo.backout_start'
        db.delete_column('sd1_events_eventinfo', 'backout_start')

        # Adding field 'EventInfo.bga_blackout_start'
        db.add_column('sd1_events_eventinfo', 'bga_blackout_start', self.gf('django.db.models.fields.DateField')(default=''), keep_default=False)

        # Adding field 'EventInfo.build_backout_start'
        db.add_column('sd1_events_eventinfo', 'build_backout_start', self.gf('django.db.models.fields.DateField')(default=''), keep_default=False)


    def backwards(self, orm):
        
        # User chose to not deal with backwards NULL issues for 'EventInfo.backout_start'
        raise RuntimeError("Cannot reverse this migration. 'EventInfo.backout_start' and its values cannot be restored.")

        # Deleting field 'EventInfo.bga_blackout_start'
        db.delete_column('sd1_events_eventinfo', 'bga_blackout_start')

        # Deleting field 'EventInfo.build_backout_start'
        db.delete_column('sd1_events_eventinfo', 'build_backout_start')


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
        'sd1_events.eventinfo': {
            'Meta': {'object_name': 'EventInfo'},
            'bga_blackout_start': ('django.db.models.fields.DateField', [], {}),
            'build_backout_start': ('django.db.models.fields.DateField', [], {}),
            'build_cap': ('django.db.models.fields.IntegerField', [], {'default': '50'}),
            'event_end': ('django.db.models.fields.DateField', [], {}),
            'event_start': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'season': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'sd1_events.eventregistration': {
            'Meta': {'object_name': 'EventRegistration'},
            'amount_paid': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '10', 'decimal_places': '2'}),
            'attended': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'due': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '10', 'decimal_places': '2'}),
            'eeps': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sd1_events.EventInfo']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'sd1_events.registrationoptions': {
            'Meta': {'object_name': 'RegistrationOptions'},
            'cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sd1_events.EventInfo']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'limit': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'new_discount': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'})
        }
    }

    complete_apps = ['sd1_events']
