import datetime


from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils.timezone import utc
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.db.models import F, Q

from sd1_events.models import *
from sd1_condenser.models import *


class Command(BaseCommand):
    help = 'Enable build buying for everyone who attended the latest event'

    def handle(self, *args, **options):
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        event = EventInfo.objects.filter(event_end__lt=now).order_by('-event_end')[0]
        print 'Doing post-game for {event}'.format(event=str(event))

        regs = event.eventregistration_set.filter(attended=True).exclude(user__is_superuser=True)
        
        for reg in regs:
            if reg.char:
                reg.char.can_buy_build = True
                reg.char.is_new = False
                reg.char.save()

                try:
                    eeps_bank = reg.user.eepsbank
                except:
                    eeps_bank = EepsBank()
                    eeps_bank.user = reg.user
                    eeps_bank.save()

                EepsBank.objects.filter(pk=eeps_bank.pk).update(eeps=F('eeps')+reg.eeps)

                eeps_record = EepsRecord()
                eeps_record.user = reg.user
                eeps_record.eeps = reg.eeps
                eeps_record.reason = '{event} post game eeps'.format(event=str(event))
                eeps_record.save()

            current_site = Site.objects.get(id=settings.SITE_ID)

            message = render_to_string('events/admin/event_post_game_email.txt', {'event': event, 'reg': reg, 'site':current_site, })

            send_mail('Second Dawn - {event} report card'.format(event=str(event)), 
                    message,
                    settings.EMAIL_FROM,
                    [reg.user.email], fail_silently=False)


