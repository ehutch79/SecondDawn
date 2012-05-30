from django.contrib.auth.models import User
from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.exceptions import NotFound

from sd1_condenser.models import Character, Skill, Profession, Header, Faction, Feat, FactionStatus, SkillBought, FeatBought, ProfessionBought

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['first_name', 'last_name', 'email']

class CharacterResource(ModelResource):
    user = fields.ToOneField(UserResource, 'user', full=True)
    skills = fields.ToManyField('sd1_condenser.api.SkillBoughtResource', 'skills', full=True)
    professions = fields.ToManyField('sd1_condenser.api.ProfessionBoughtResource', 'professions', full=True)
    headers = fields.ToManyField('sd1_condenser.api.HeaderResource', 'headers', full=True)
    factions = fields.ToManyField('sd1_condenser.api.FactionStatusResource', lambda bundle: FactionStatus.objects.filter(char=bundle.obj, member=True), full=True)
    feats = fields.ToManyField('sd1_condenser.api.FeatBoughtResource', 'feats', full=True)

    def obj_get_list(self, request=None, **kwargs):
        obj_list = super(CharacterResource, self).obj_get_list(request, **kwargs)

        if not request.user.is_superuser:
            obj_list = obj_list.filter(user=request.user)

        return obj_list

    def obj_get(self, request=None, **kwargs):
        obj = super(CharacterResource, self).obj_get(request, **kwargs)

        if obj.user != request.user and not request.user.is_superuser:
            raise NotFound

        return obj


    class Meta:
        queryset = Character.objects.all()
        resource_name = 'char'


class SkillResource(ModelResource):
    headers = fields.ToManyField('sd1_condenser.api.HeaderResource', 'headers', full=True,  blank=True, null=True)
    required_skills = fields.ToManyField('sd1_condenser.api.SkillResource', 'required_skills', full=True, blank=True, null=True)
    grants = fields.ToManyField('sd1_condenser.api.SkillResource', 'grants', full=True, blank=True, null=True)

    def obj_get_list(self, request=None, **kwargs):
        obj_list = super(SkillResource, self).obj_get_list(request, **kwargs)

        if not request.user.is_superuser and not request.user.is_staff:
            obj_list = obj_list.filter(playable=True)

        return obj_list

    class Meta:
        queryset = Skill.objects.all()
        resource_name = 'skills'
        limit = 0
        ordering = ['name']


class ProfessionResource(ModelResource):
    class Meta:
        queryset = Profession.objects.all()
        resource_name = 'professions'
        limit = 0
        ordering = ['name']

class ProfessionBoughtResource(ModelResource):
    profession = fields.ToOneField(ProfessionResource, 'profession', full=True)
    class Meta:
        queryset = ProfessionBought.objects.all()
        resource_name = 'professionbought'

class SkillBoughtResource(ModelResource):
    skill = fields.ToOneField(SkillResource, 'skill', full=True)
    bundled_from = fields.ToOneField(SkillResource, 'bundled_from', full=True, blank=True, null=True)
    paid_total = fields.IntegerField(readonly=True, attribute='paid_total')
    class Meta:
        queryset = SkillBought.objects.all()
        resource_name = 'skillbought'


class FeatResource(ModelResource):
    
    class Meta:
        queryset = Feat.objects.all()
        resource_name = 'feat'
        limit = 0
        ordering = ['name']


class FeatBoughtResource(ModelResource):
    feat = fields.ToOneField(FeatResource, 'feat', full=True)
    paid_total = fields.IntegerField(readonly=True, attribute='paid_total')

    class Meta:
        queryset = FeatBought.objects.all()
        resource_name = 'featbought'

class HeaderResource(ModelResource):

    class Meta:
        queryset = Header.objects.all()
        resource_name = 'headers'

class FactionResource(ModelResource):

    def obj_get_list(self, request=None, **kwargs):
        obj_list = super(FactionResource, self).obj_get_list(request, **kwargs)

        return obj_list

    class Meta:
        queryset = Faction.objects.all()
        resource_name = 'faction'
        excludes = ['playable', ]


class FactionStatusResource(ModelResource):
    faction = fields.ToOneField(FactionResource, 'faction', full=True)
    
    class Meta:
        queryset = FactionStatus.objects.all()
        resource_name = 'factionstatus'
        excludes = ['rep', ]
