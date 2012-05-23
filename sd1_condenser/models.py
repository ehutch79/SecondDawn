import math
from django.db import models
from django.db.models import Q
from django.db.models import Avg, Max, Min, Count
from django.contrib.auth.models import User

from django_extensions.db.fields import AutoSlugField, UUIDField

from django.db.models.signals import post_save
from django.dispatch import receiver


class PersonalProfile(models.Model):
    id = UUIDField(version=4, primary_key=True)
    user = models.OneToOneField(User, db_index=True)

    is_first_responder = models.BooleanField(default=False, verbose_name="First Responder",
                                             help_text="Are you an EMT/Reg. Nurse?")
    is_veggie = models.BooleanField(default=False, verbose_name="Vegetarian")
    is_glutard = models.BooleanField(default=False, verbose_name="Gluten Intolerance")
    is_lactard = models.BooleanField(default=False, verbose_name="Lactose Intolerance")
    is_allergic = models.BooleanField(default=False, verbose_name="Misc. Allergies (spec. below)")
    allergies = models.TextField(verbose_name="Allergy specifics and other preferences", blank=True, null=True)
    medical = models.TextField(verbose_name="Medical considerations", blank=True, null=True)

    stripe_customer = models.CharField(max_length=256, null=True, blank=True)

    def __unicode__(self):
        return self.user.email

    def get_current_char(self):
        chars = Character.objects.filter(is_deceased=False, is_retired=False, is_npc=False, user=self.user)
        
        if self.user.is_staff or self.user.is_superuser:
            return None
        if chars.count() > 1:
            return 'Multiple Chars'
        if chars.count() == 1:
            return chars[0]
        else:
            return None

    def get_prev_char(self):
        chars = Character.objects.filter(Q(is_deceased=True) | Q(is_retired=True), is_npc=False, user=self.user)
        return chars

class EepsBank(models.Model):
    id = UUIDField(version=4, primary_key=True)
    user = models.OneToOneField(User, db_index=True, editable=False)

    eeps = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.email

class EepsRecord(models.Model):
    id = UUIDField(version=4, primary_key=True)
    user = models.ForeignKey(User, db_index=True, editable=False)

    eeps = models.IntegerField(default=0, editable=False)
    reason = models.TextField(blank=True, null=True)

    when = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.user.email

    class Meta:
        ordering = ['when',]

class ContactInfo(models.Model):
    CONTACTTYPE_CHOICES = (
        ('phone', 'Phone'),
        ('cell', 'Cell'),
        ('emergency', 'Emergency Contact Ph.'),
        ('email', 'EMail'),
        )

    id = UUIDField(version=4, primary_key=True)
    user = models.ForeignKey(User, db_index=True, editable=False)

    type = models.CharField(max_length=250, verbose_name="contact method", choices=CONTACTTYPE_CHOICES)
    details = models.CharField(max_length=250, verbose_name="contact details")


class Faction(models.Model):
    id = UUIDField(version=4, primary_key=True)
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', overwrite=True)
    beginner = models.BooleanField(default=False)
    playable = models.BooleanField(default=False)
    description = models.TextField()
    start_gear = models.TextField()

    def __unicode__(self):
        return self.name

    def player_members(self):
        return self.standings.filter(char__is_npc=False,char__is_deceased=False,char__is_retired=False)


class Header(models.Model):
    id = UUIDField(version=4, primary_key=True)
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', overwrite=True)
    description = models.TextField()
    ability = models.TextField(verbose_name="header ability")

    def __unicode__(self):
        return self.name

    def player_members(self):
        return self.character_set.filter(is_npc=False,is_deceased=False,is_retired=False)


class Profession(models.Model):
    id = UUIDField(version=4, primary_key=True)
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', overwrite=True)
    description = models.TextField()

    def __unicode__(self):
        return self.name

    def player_members(self):
        return self.bought_by.filter(char__is_npc=False,char__is_deceased=False,char__is_retired=False)

    def max_score(self):
        return self.bought_by.aggregate(max_score=Max('score'))



class Skill(models.Model):
    id = UUIDField(version=4, primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(populate_from='name', overwrite=True)
    playable = models.BooleanField(default=True, help_text="Is this skill available to players?")

    description = models.TextField()
    game_effects = models.TextField()

    build_cost = models.IntegerField(default=0)
    activation = models.CharField(max_length=255, blank=True, null=True)

    headers = models.ManyToManyField(Header, blank=True, null=True,
                                     help_text="if blank, no req. If multiple, any will qualify")
    required_skills = models.ManyToManyField('self', symmetrical=False, related_name="dependant_skills", blank=True,
                                             null=True, help_text="if blank then none. if multiple, all req to learn")

    grants = models.ManyToManyField('self', symmetrical=False, related_name="+", blank=True, null=True,
                                    help_text="learning this will automatically add these skills free")

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Feat(models.Model):
    id = UUIDField(version=4, primary_key=True)
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', overwrite=True)

    requires_info = models.BooleanField(default=False)
    cost = models.IntegerField(default=0)
    incr_cost = models.IntegerField(default=0)

    description = models.TextField()

    def __unicode__(self):
        return self.name


class Character(models.Model):
    id = UUIDField(version=4, primary_key=True)
    user = models.ForeignKey(User, db_index=True, editable=True, blank=True, null=True)
    slug = AutoSlugField(populate_from='name', overwrite=True)

    build_spent = models.IntegerField(default=0)
    free_build = models.IntegerField(default=40)

    is_npc = models.BooleanField(default=False)

    is_retired = models.BooleanField(default=False)
    is_deceased = models.BooleanField(default=False)

    is_new = models.BooleanField(default=True)
    is_updated = models.BooleanField(default=False)

    can_buy_build = models.BooleanField(default=True)

    name = models.CharField(max_length=255)

    headers = models.ManyToManyField(Header, blank=True, null=True)

    blood = models.IntegerField(default=1)
    might = models.IntegerField(default=1)
    mind = models.IntegerField(default=1)
    finesse = models.IntegerField(default=1)
    will = models.IntegerField(default=1)

    background = models.TextField(blank=True, null=True)
    background_approved = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ['-created']

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('sd1_condenser.views.character_view', (), { 'slug': self.slug } )

    def available_skills(self):
        skills = list()
        SkillQS = Skill.objects.all()
        if not self.is_npc:
            SkillQS = SkillQS.filter(playable=True)

        for skill in SkillQS:
            tags = ""
            if skill in self.skills.all():
                tags += ' taken'

            if skill.headers.count():
                has_header = False
                for header in skill.headers.all():
                    if header in self.headers.all():
                        has_header = True

                if not has_header:
                    tags += ' missing-req missing-header'

            if skill.required_skills.count():
                has_skills = True
                for req in skill.required_skills.all():
                    if req not in self.skills.all():
                        has_skills = False

                if not has_skills:
                    tags += 'missing-req missing-skill'

            if not tags:
                tags = "available"

            skills.append({
                'tags': tags,
                'skill': skill
            })

        return skills

class SkillBought(models.Model):
    id = UUIDField(version=4, primary_key=True)
    
    char = models.ForeignKey(Character, db_index=True, related_name="skills")
    skill = models.ForeignKey(Skill, db_index=True, related_name="bought_by")

    bundled_from = models.ForeignKey(Skill, blank=True, null=True)
    paid_total = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Skills Bought"

    def __unicode__(self):
        return self.skill.name

class FeatBought(models.Model):
    id = UUIDField(version=4, primary_key=True)
    
    char = models.ForeignKey(Character, db_index=True, related_name="feats")
    feat = models.ForeignKey(Feat, db_index=True, related_name="bought_by")
    
    info = models.CharField(max_length=255)

    paid_total = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Feat Bought"
        verbose_name_plural = "Feats Bought"

    def __unicode__(self):
        if self.info:
            return "{feat} ({info})".format(feat=self.feat.name, info=self.info)

        return self.feat.name



class FactionStatus(models.Model):
    id = UUIDField(version=4, primary_key=True)
    
    char = models.ForeignKey(Character, db_index=True, related_name="factions")
    faction = models.ForeignKey(Faction, db_index=True, related_name="standings")

    member = models.BooleanField(default=False)
    rep = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Faction Standing"
        verbose_name_plural = "Faction Standings"

    def __unicode__(self):
        return self.faction.name

class ProfessionBought(models.Model):
    id = UUIDField(version=4, primary_key=True)
    
    char = models.ForeignKey(Character, db_index=True, editable=False, blank=True, null=True, related_name="professions")
    profession = models.ForeignKey(Profession, db_index=True, related_name="bought_by")
    score = models.IntegerField(default=5)

    def calc_cost_to(self, start, score):
        cost = 0
        
        while score > start:
            cost += int(score/10)
            if score%10:
                cost += 1
            score -= 1;
        return cost

    class Meta:
        verbose_name_plural = "Professions Bought"


class ProfSkill(models.Model):
    id = UUIDField(version=4, primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(populate_from='name', overwrite=True)
    playable = models.BooleanField(default=True, help_text="Is this available for players to buy?")

    components = models.BooleanField(default=False, help_text="Requires components")

    description = models.TextField()
    requires_novel = models.BooleanField(default=False, help_text="Does the player need to type a novel to use")

    cost = models.IntegerField(default=0)
    incr_cost = models.IntegerField(default=0)
    variable_cost = models.BooleanField(default=False, help_text="cost to buy can vary")

    rank = models.IntegerField(default=1)

    profession = models.ManyToManyField(Profession)
    
    required_skills = models.ManyToManyField('self', symmetrical=False, related_name="dependant_skills", blank=True,
                                             null=True, help_text="if blank then none. if multiple, all req to learn")

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['rank', 'name',]


class ProfSkillLearned(models.Model):
    id = UUIDField(version=4, primary_key=True)

    char = models.ForeignKey(Character, related_name="profession_skills")
    skill = models.ForeignKey(ProfSkill)

    pp_paid = models.IntegerField(default=0)
    specifics = models.CharField(max_length=255, blank=True, null=True)

    novel = models.TextField(null=True, blank=True)


class BGAction(models.Model):
    id = UUIDField(version=4, primary_key=True)
    user = models.ForeignKey(User, db_index=True, editable=True, blank=True, null=True)
    
    event = models.ForeignKey('sd1_events.EventInfo', db_index=True, editable=True, blank=True, null=True)
    is_ingame = models.BooleanField(default=False)

    action = models.CharField(max_length=255)

    profession = models.ForeignKey(ProfessionBought, db_index=True, editable=True, blank=True, null=True)

    details = models.TextField(blank=True, null=True)

    pending = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)


class ProfessionAction(models.Model):
    id = UUIDField(version=4, primary_key=True)
    bga = models.ForeignKey(BGAction, db_index=True, editable=True, blank=True, null=True)
    
    use = models.BooleanField(default=False)
    learn = models.BooleanField(default=False)
    pp_spent = models.IntegerField(default=0)
    partial_spend = models.BooleanField(default=False)
    
    prof_skill = models.ForeignKey(ProfSkill, blank=True, null=True)

    specifics = models.TextField(blank=True, null=True)

    novel = models.TextField(null=True, blank=True)



@receiver(post_save, sender=User)
def make_profiles(sender, **kwargs):
    user = kwargs['instance']

    try:
        eeps = user.eepsbank
    except:
        eeps = EepsBank()
        eeps.user = user

    try:
        prof = user.personalprofile
    except:
        prof = PersonalProfile()
        prof.user = user

    try:
        eeps.save()
        prof.save()
    except:
        pass

