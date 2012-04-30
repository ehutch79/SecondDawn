from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.conf import settings
from django_extensions.db.fields import AutoSlugField, UUIDField


class EventInfo(models.Model):
    id = UUIDField(version=4, primary_key=True)
    season = models.IntegerField(default=0)
    name = models.CharField(max_length=250, help_text="i.e. Event 1, Event 2, Winter Feast, etc")

    build_cap = models.IntegerField(default=50)

    bga_blackout_start = models.DateField(help_text="No bgas submitted after this date")
    build_blackout_start = models.DateField(help_text="No build or eeps spent after this")
    event_start = models.DateField(help_text="Game on")
    event_end = models.DateField(help_text="Game off")

    def __unicode__(self):
        return 'Season {season} - {event_name}'.format(season=self.season, event_name=self.name)

    def total_regs(self):
        return self.eventregistration_set.count()
    total_regs.short_description = 'Total Registrations'


    class Meta:
        ordering = ['event_start']
        verbose_name = "Event"
        verbose_name_plural = "Events"

class RegistrationOptions(models.Model):
    id = UUIDField(version=4, primary_key=True)
    event = models.ForeignKey(EventInfo, db_index=True)
    
    name = models.CharField(max_length=250)
    limit = models.IntegerField(default=0)
    cost = models.DecimalField(decimal_places=2, max_digits=10)
    new_discount = models.DecimalField(decimal_places=2, max_digits=10)

    npc = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['-cost']
        verbose_name = "Registration Option"
        verbose_name_plural = "Registration Options"


class EventRegistration(models.Model):
    id = UUIDField(version=4, primary_key=True)
    user = models.ForeignKey(User, db_index=True)
    event = models.ForeignKey(EventInfo, db_index=True)
    option = models.ForeignKey(RegistrationOptions, db_index=True)

    due = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    paid = models.BooleanField(default=False)
    amount_paid = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)

    attended = models.BooleanField(default=False)
    eeps = models.IntegerField(default=0)
    
    reportcard_submitted = models.BooleanField(default=False)

    def __unicode__(self):
        return '{fname} {lname} ({email}) attending {event}'.format(fname=self.user.first_name, lname=self.user.last_name, email=self.user.email, event=self.event)

    class Meta:
        ordering = ['event__event_start']
        verbose_name = "Player Registration"
        verbose_name_plural = "Player Registrations"


class Receipt(models.Model):
    id = UUIDField(version=4, primary_key=True)
    user = models.ForeignKey(User, db_index=True)

    regs = models.ManyToManyField(EventRegistration, verbose_name="registrations")
    total = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    when = models.DateTimeField(auto_now_add=True)

    paid = models.BooleanField(default=False)

    stripe_charge = models.CharField(max_length=250, editable=False, null=True, blank=True)
    problem = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return '{email} receipt'.format(email=self.user.email)

class ReportCard(models.Model):
    id = UUIDField(version=4, primary_key=True)
    reg = models.OneToOneField(EventRegistration, db_index=True)

    submitted = models.DateTimeField(auto_now=True)

    enjoy_yourself = models.BooleanField(default=False)
    likely_to_return = models.BooleanField(default=False)

    rules = models.IntegerField(default=0)
    food = models.IntegerField(default=0)
    puzzles = models.IntegerField(default=0)
    role_playing = models.IntegerField(default=0)
    costumes = models.IntegerField(default=0)
    overall = models.IntegerField(default=0)

    anyone_help = models.TextField(blank=True, null=True)

    plots = models.TextField(blank=True, null=True)
    goals = models.TextField(blank=True, null=True)

    comments = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return 'report card'







