from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from django.db.models.signals import post_save
from django.dispatch import receiver

from django_extensions.db.fields import AutoSlugField, UUIDField

class Profile(models.Model):
    id = UUIDField(version=4, primary_key=True)
    user = models.OneToOneField(User, db_index=True, editable=False)
    
    slug = AutoSlugField(populate_from='display_name', overwrite=True)
    
    display_name = models.CharField(max_length=75)
    
    def __unicode__(self):
        return self.display_name

class ActivityLog(models.Model):
    TYPE_CHOICES = (
        ('alert', 'Alert'),
        ('notice', 'Notice'),
        ('info', 'Info'),
    )

    id = UUIDField(version=4, primary_key=True)
    user = models.ForeignKey(User, null=True, blank=True, db_index=True, editable=False)
    
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, db_index=True, default="info")
    ip = models.CharField(max_length=256)
    user_agent = models.CharField(max_length=1024)
    action = models.CharField(max_length=1024)
    
    target_type = models.ForeignKey(ContentType, blank=True, null=True)
    target_pk = models.PositiveIntegerField(blank=True, null=True)
    target = generic.GenericForeignKey('target_type', 'target_pk')
    
    new = models.BooleanField(default=True, db_index=True)
    when = models.DateTimeField(auto_now_add=True)
    

class SocialNetworkLink(models.Model):
    NETWORK_CHOICES = (
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('linkedin', 'LinkedIn'),
        ('flickr', 'Flickr'),
        ('website', 'Website'),
    )
    
    id = UUIDField(version=4, primary_key=True)
    user = models.ForeignKey(User, db_index=True, editable=False)
    
    network = models.CharField(max_length=100, choices=NETWORK_CHOICES, verbose_name="social network")
    link = models.URLField()
    name = models.CharField(max_length=100, verbose_name="display name")
    


@receiver(post_save, sender=User)
def make_profile(sender, **kwargs):
    user = kwargs['instance']

    try:
        profile = user.get_profile()
    except:
        profile = Profile()
        profile.user = user

    if not profile.display_name:
        profile.display_name = '{first} {last}'.format(first=user.first_name, last=user.last_name)

    profile.save()
