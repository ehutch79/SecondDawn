from django.contrib import admin
from sd1_condenser.models import *

class CharFactionStatus(admin.TabularInline):
    model = FactionStatus
    fk_name = "char"
    extra = 0

class CharSkills(admin.TabularInline):
    model = SkillBought
    fk_name = "char"
    readonly_fields = ['bundled_from',]
    extra = 0

class CharFeats(admin.TabularInline):
    model = FeatBought
    fk_name = "char"
    extra = 0

class ProfBoughtStatus(admin.TabularInline):
    model = ProfessionBought
    fk_name = "char"
    extra = 0

class CharacterAdmin(admin.ModelAdmin):
    inlines = [CharFactionStatus, CharSkills, ProfBoughtStatus, CharFeats, ]
    list_display = ('name', 'is_new', 'is_npc', 'is_deceased', 'is_retired', 'background_approved')
    list_filter = ('is_new', 'is_npc', 'is_deceased', 'is_retired', 'background_approved')
    search_fields = ['user__email', 'name', ]

admin.site.register(Character, CharacterAdmin)

class HeaderAdmin(admin.ModelAdmin):
    pass
admin.site.register(Header, HeaderAdmin)

class FactionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Faction, FactionAdmin)

class ProfessionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Profession, ProfessionAdmin)

class FeatAdmin(admin.ModelAdmin):
    pass
admin.site.register(Feat, FeatAdmin)


class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'build_cost', 'activation')
    list_display_links = ('name', )
    search_fields = ['name', 'description', 'game_effects' ]

admin.site.register(Skill, SkillAdmin)


class ProfileAdmin(admin.ModelAdmin):
    pass
admin.site.register(PersonalProfile, ProfileAdmin)

class EepsRecordAdmin(admin.ModelAdmin):
    readonly_fields = ['eeps', 'when', ]
    list_display = ('__unicode__', 'eeps', 'reason', 'when', )
admin.site.register(EepsRecord, EepsRecordAdmin)
