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

        regs = event.eventregistration_set.exclude(user__is_superuser=True)
 
        for reg in regs:
            if reg.char:
                reg.char.can_buy_build = True
                reg.char.is_new = False
                reg.char.is_updated = False
                reg.char.save()
 
#            current_site = Site.objects.get(id=settings.SITE_ID)

#            message = render_to_string('events/admin/event_post_game_email.txt', {'event': event, 'reg': reg, 'site':current_site, })
            
            if not reg.admin_hold:
                pass
#                send_mail('Second Dawn - {event} report card'.format(event=str(event)), 
#                    message,
#                    settings.EMAIL_FROM,
#                    [reg.user.email], fail_silently=False)


