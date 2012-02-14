import math
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

from django_extensions.db.fields import AutoSlugField, UUIDField


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

    def __unicode__(self):
        return self.user.email



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


class Header(models.Model):
    id = UUIDField(version=4, primary_key=True)
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', overwrite=True)
    description = models.TextField()
    ability = models.TextField(verbose_name="header ability")

    def __unicode__(self):
        return self.name


class Profession(models.Model):
    id = UUIDField(version=4, primary_key=True)
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', overwrite=True)
    description = models.TextField()

    def __unicode__(self):
        return self.name


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

    def __unicode__(self):
        return self.name


class Character(models.Model):
    id = UUIDField(version=4, primary_key=True)
    user = models.ForeignKey(User, db_index=True, editable=False, blank=True, null=True)
    slug = AutoSlugField(populate_from='name', overwrite=True)

    build_spent = models.IntegerField(default=0)
    free_build = models.IntegerField(default=40)

    is_npc = models.BooleanField(default=False)

    is_retired = models.BooleanField(default=False)
    is_deceased = models.BooleanField(default=False)

    is_new = models.BooleanField(default=True)

    can_spend_eeps = models.BooleanField(default=True)

    name = models.CharField(max_length=255)

    headers = models.ManyToManyField(Header, blank=True, null=True)

    blood = models.IntegerField(default=1)
    might = models.IntegerField(default=1)
    mind = models.IntegerField(default=1)
    finesse = models.IntegerField(default=1)
    will = models.IntegerField(default=1)

    background = models.TextField(blank=True, null=True)
    background_approved = models.BooleanField(default=False)

    feats = models.ManyToManyField(Feat, blank=True, null=True)


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
