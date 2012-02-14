# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Feat'
        db.create_table('sd1_condenser_feat', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('sd1_condenser', ['Feat'])

        # Adding model 'Profession'
        db.create_table('sd1_condenser_profession', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('sd1_condenser', ['Profession'])

        # Adding model 'Character'
        db.create_table('sd1_condenser_character', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('slug', self.gf('django_extensions.db.fields.AutoSlugField')(allow_duplicates=False, max_length=50, separator=u'-', blank=True, populate_from='name', overwrite=True, db_index=True)),
            ('build_spent', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('free_build', self.gf('django.db.models.fields.IntegerField')(default=40)),
            ('is_npc', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_retired', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_deceased', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_new', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('blood', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('might', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('mind', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('finesse', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('will', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('background', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('background_approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('sd1_condenser', ['Character'])

        # Adding M2M table for field factions on 'Character'
        db.create_table('sd1_condenser_character_factions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('character', models.ForeignKey(orm['sd1_condenser.character'], null=False)),
            ('faction', models.ForeignKey(orm['sd1_condenser.faction'], null=False))
        ))
        db.create_unique('sd1_condenser_character_factions', ['character_id', 'faction_id'])

        # Adding M2M table for field headers on 'Character'
        db.create_table('sd1_condenser_character_headers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('character', models.ForeignKey(orm['sd1_condenser.character'], null=False)),
            ('header', models.ForeignKey(orm['sd1_condenser.header'], null=False))
        ))
        db.create_unique('sd1_condenser_character_headers', ['character_id', 'header_id'])

        # Adding M2M table for field skills on 'Character'
        db.create_table('sd1_condenser_character_skills', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('character', models.ForeignKey(orm['sd1_condenser.character'], null=False)),
            ('skill', models.ForeignKey(orm['sd1_condenser.skill'], null=False))
        ))
        db.create_unique('sd1_condenser_character_skills', ['character_id', 'skill_id'])

        # Adding M2M table for field feats on 'Character'
        db.create_table('sd1_condenser_character_feats', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('character', models.ForeignKey(orm['sd1_condenser.character'], null=False)),
            ('feat', models.ForeignKey(orm['sd1_condenser.feat'], null=False))
        ))
        db.create_unique('sd1_condenser_character_feats', ['character_id', 'feat_id'])

        # Adding M2M table for field professions on 'Character'
        db.create_table('sd1_condenser_character_professions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('character', models.ForeignKey(orm['sd1_condenser.character'], null=False)),
            ('profession', models.ForeignKey(orm['sd1_condenser.profession'], null=False))
        ))
        db.create_unique('sd1_condenser_character_professions', ['character_id', 'profession_id'])

        # Adding model 'Header'
        db.create_table('sd1_condenser_header', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('ability', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('sd1_condenser', ['Header'])

        # Adding model 'Faction'
        db.create_table('sd1_condenser_faction', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('start_gear', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('sd1_condenser', ['Faction'])

        # Adding model 'Skill'
        db.create_table('sd1_condenser_skill', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('game_effects', self.gf('django.db.models.fields.TextField')()),
            ('build_cost', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('activation', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('sd1_condenser', ['Skill'])

        # Adding M2M table for field headers on 'Skill'
        db.create_table('sd1_condenser_skill_headers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('skill', models.ForeignKey(orm['sd1_condenser.skill'], null=False)),
            ('header', models.ForeignKey(orm['sd1_condenser.header'], null=False))
        ))
        db.create_unique('sd1_condenser_skill_headers', ['skill_id', 'header_id'])


    def backwards(self, orm):
        
        # Deleting model 'Feat'
        db.delete_table('sd1_condenser_feat')

        # Deleting model 'Profession'
        db.delete_table('sd1_condenser_profession')

        # Deleting model 'Character'
        db.delete_table('sd1_condenser_character')

        # Removing M2M table for field factions on 'Character'
        db.delete_table('sd1_condenser_character_factions')

        # Removing M2M table for field headers on 'Character'
        db.delete_table('sd1_condenser_character_headers')

        # Removing M2M table for field skills on 'Character'
        db.delete_table('sd1_condenser_character_skills')

        # Removing M2M table for field feats on 'Character'
        db.delete_table('sd1_condenser_character_feats')

        # Removing M2M table for field professions on 'Character'
        db.delete_table('sd1_condenser_character_professions')

        # Deleting model 'Header'
        db.delete_table('sd1_condenser_header')

        # Deleting model 'Faction'
        db.delete_table('sd1_condenser_faction')

        # Deleting model 'Skill'
        db.delete_table('sd1_condenser_skill')

        # Removing M2M table for field headers on 'Skill'
        db.delete_table('sd1_condenser_skill_headers')


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
        'sd1_condenser.character': {
            'Meta': {'object_name': 'Character'},
            'background': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'background_approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'blood': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'build_spent': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'factions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sd1_condenser.Faction']", 'symmetrical': 'False'}),
            'feats': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sd1_condenser.Feat']", 'symmetrical': 'False'}),
            'finesse': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'free_build': ('django.db.models.fields.IntegerField', [], {'default': '40'}),
            'headers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sd1_condenser.Header']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'is_deceased': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_new': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_npc': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_retired': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'might': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'mind': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'professions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sd1_condenser.Profession']", 'symmetrical': 'False'}),
            'skills': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sd1_condenser.Skill']", 'symmetrical': 'False'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'name'", 'overwrite': 'True', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'will': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'sd1_condenser.contactinfo': {
            'Meta': {'object_name': 'ContactInfo'},
            'details': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'sd1_condenser.faction': {
            'Meta': {'object_name': 'Faction'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'start_gear': ('django.db.models.fields.TextField', [], {})
        },
        'sd1_condenser.feat': {
            'Meta': {'object_name': 'Feat'},
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'sd1_condenser.header': {
            'Meta': {'object_name': 'Header'},
            'ability': ('django.db.models.fields.TextField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'sd1_condenser.personalprofile': {
            'Meta': {'object_name': 'PersonalProfile'},
            'allergies': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'is_allergic': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_first_responder': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_glutard': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_lactard': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_veggie': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'medical': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'sd1_condenser.profession': {
            'Meta': {'object_name': 'Profession'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'sd1_condenser.skill': {
            'Meta': {'object_name': 'Skill'},
            'activation': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'build_cost': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'game_effects': ('django.db.models.fields.TextField', [], {}),
            'headers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sd1_condenser.Header']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['sd1_condenser']
