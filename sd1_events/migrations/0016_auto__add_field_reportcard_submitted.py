# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'ReportCard.submitted'
        db.add_column('sd1_events_reportcard', 'submitted', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2012, 4, 30, 15, 17, 18, 544511), blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'ReportCard.submitted'
        db.delete_column('sd1_events_reportcard', 'submitted')


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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 4, 30, 15, 17, 18, 552622)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 4, 30, 15, 17, 18, 552423)'}),
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
            'Meta': {'ordering': "['event_start']", 'object_name': 'EventInfo'},
            'bga_blackout_start': ('django.db.models.fields.DateField', [], {}),
            'build_blackout_start': ('django.db.models.fields.DateField', [], {}),
            'build_cap': ('django.db.models.fields.IntegerField', [], {'default': '50'}),
            'event_end': ('django.db.models.fields.DateField', [], {}),
            'event_start': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'season': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'sd1_events.eventregistration': {
            'Meta': {'ordering': "['event__event_start']", 'object_name': 'EventRegistration'},
            'amount_paid': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '10', 'decimal_places': '2'}),
            'attended': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'due': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '10', 'decimal_places': '2'}),
            'eeps': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sd1_events.EventInfo']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'option': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sd1_events.RegistrationOptions']"}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reportcard_submitted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'sd1_events.receipt': {
            'Meta': {'object_name': 'Receipt'},
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'problem': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'regs': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sd1_events.EventRegistration']", 'symmetrical': 'False'}),
            'stripe_charge': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'total': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '10', 'decimal_places': '2'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'when': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'sd1_events.registrationoptions': {
            'Meta': {'ordering': "['-cost']", 'object_name': 'RegistrationOptions'},
            'cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sd1_events.EventInfo']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'limit': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'new_discount': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'npc': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'sd1_events.reportcard': {
            'Meta': {'object_name': 'ReportCard'},
            'anyone_help': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'costumes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'enjoy_yourself': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'food': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'goals': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'likely_to_return': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'overall': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'plots': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'puzzles': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'reg': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sd1_events.EventRegistration']", 'unique': 'True'}),
            'role_playing': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rules': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'submitted': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['sd1_events']
