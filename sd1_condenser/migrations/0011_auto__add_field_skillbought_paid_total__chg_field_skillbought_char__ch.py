# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'SkillBought.paid_total'
        db.add_column('sd1_condenser_skillbought', 'paid_total', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Changing field 'SkillBought.char'
        db.alter_column('sd1_condenser_skillbought', 'char_id', self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['sd1_condenser.Character']))

        # Changing field 'SkillBought.skill'
        db.alter_column('sd1_condenser_skillbought', 'skill_id', self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['sd1_condenser.Skill']))

        # Changing field 'FactionStatus.char'
        db.alter_column('sd1_condenser_factionstatus', 'char_id', self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['sd1_condenser.Character']))

        # Changing field 'FactionStatus.faction'
        db.alter_column('sd1_condenser_factionstatus', 'faction_id', self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['sd1_condenser.Faction']))


    def backwards(self, orm):
        
        # Deleting field 'SkillBought.paid_total'
        db.delete_column('sd1_condenser_skillbought', 'paid_total')

        # Changing field 'SkillBought.char'
        db.alter_column('sd1_condenser_skillbought', 'char_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['sd1_condenser.Character']))

        # Changing field 'SkillBought.skill'
        db.alter_column('sd1_condenser_skillbought', 'skill_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['sd1_condenser.Skill']))

        # Changing field 'FactionStatus.char'
        db.alter_column('sd1_condenser_factionstatus', 'char_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['sd1_condenser.Character']))

        # Changing field 'FactionStatus.faction'
        db.alter_column('sd1_condenser_factionstatus', 'faction_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['sd1_condenser.Faction']))


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
            'feats': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['sd1_condenser.Feat']", 'null': 'True', 'blank': 'True'}),
            'finesse': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'free_build': ('django.db.models.fields.IntegerField', [], {'default': '40'}),
            'headers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['sd1_condenser.Header']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'is_deceased': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_new': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_npc': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_retired': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'might': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'mind': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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
            'beginner': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'playable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'name'", 'overwrite': 'True', 'db_index': 'True'}),
            'start_gear': ('django.db.models.fields.TextField', [], {})
        },
        'sd1_condenser.factionstatus': {
            'Meta': {'object_name': 'FactionStatus'},
            'char': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'factions'", 'to': "orm['sd1_condenser.Character']"}),
            'faction': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'standings'", 'to': "orm['sd1_condenser.Faction']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rep': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'sd1_condenser.feat': {
            'Meta': {'object_name': 'Feat'},
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'name'", 'overwrite': 'True', 'db_index': 'True'})
        },
        'sd1_condenser.header': {
            'Meta': {'object_name': 'Header'},
            'ability': ('django.db.models.fields.TextField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'name'", 'overwrite': 'True', 'db_index': 'True'})
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'name'", 'overwrite': 'True', 'db_index': 'True'})
        },
        'sd1_condenser.professionbought': {
            'Meta': {'object_name': 'ProfessionBought'},
            'char': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'professions'", 'null': 'True', 'to': "orm['sd1_condenser.Character']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pp': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'profession': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'bought_by'", 'null': 'True', 'to': "orm['sd1_condenser.Profession']"})
        },
        'sd1_condenser.skill': {
            'Meta': {'object_name': 'Skill'},
            'activation': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'build_cost': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'game_effects': ('django.db.models.fields.TextField', [], {}),
            'grants': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['sd1_condenser.Skill']"}),
            'headers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['sd1_condenser.Header']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'playable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'required_skills': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'dependant_skills'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['sd1_condenser.Skill']"}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'name'", 'overwrite': 'True', 'db_index': 'True'})
        },
        'sd1_condenser.skillbought': {
            'Meta': {'object_name': 'SkillBought'},
            'bundled_from': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sd1_condenser.Skill']", 'null': 'True', 'blank': 'True'}),
            'char': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'skills'", 'to': "orm['sd1_condenser.Character']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paid_total': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'skill': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bought_by'", 'to': "orm['sd1_condenser.Skill']"})
        }
    }

    complete_apps = ['sd1_condenser']
