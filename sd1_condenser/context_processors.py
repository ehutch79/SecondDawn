from django.conf import settings
from sd1_events.models import EventInfo
import datetime

def in_blackout(request):
    now = datetime.datetime.now()
    bga_blackout = False
    build_blackout = False
    bga_events = EventInfo.objects.filter(bga_blackout_start__lte=now, event_end__gte=now)
    if  bga_events.count() > 0:
        bga_blackout = True

    build_events = bga_events.filter(build_blackout_start__lte=now)
    if build_events.count() > 0:
        build_blackout = True
    
    return { 'in_bga_blackout': bga_blackout, 'in_build_blackout': build_blackout }
    
