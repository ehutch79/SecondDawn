import math
import datetime
import StringIO

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib import messages
from django.utils import simplejson as json
from django.contrib.auth.decorators import login_required
from django.db.models import F, Q, Avg



from django.utils.timezone import utc

import xhtml2pdf.pisa as xhtml2pdf
import stripe

from sd1_events.models import *
from sd1_condenser.models import *


import logging

logger = logging.getLogger(__name__)

@login_required
def event_list(request):
    events = EventInfo.objects.all()
    reged_events = EventRegistration.objects.filter(user=request.user).values_list('event__pk',flat=True)

    return render_to_response('events/events_list.html', {'events': events, 'reged_events': reged_events}, context_instance=RequestContext(request))

@login_required
def register_for_events(request):
    if request.method != 'POST':
        return HttpResponseForbidden('Method not allowed')
    
    event_options = request.POST.getlist('reg_option')

    total_cost = 0

    receipt = Receipt()
    receipt.user = request.user
    receipt.save()

    for event_option in event_options:
        if event_option:
            op = RegistrationOptions.objects.get(pk=event_option)

            regs = EventRegistration.objects.filter(user=request.user, event=op.event)
            if regs.count() > 0:
                continue

            reg = EventRegistration()
            reg.user = request.user
            reg.char = reg.user.personalprofile.get_current_char()
            reg.option = op
            reg.event = op.event
            reg.due = op.cost

            if request.user.eventregistration_set.count() < 1:
                reg.due -= op.new_discount

            reg.save()

            receipt.regs.add(reg)

            total_cost += reg.due

    if total_cost:
        if request.POST['payment-type']== 'cc':

            stripe.api_key = settings.STRIPE_SECRET

            token = request.POST['stripeToken']
            
            try:
                charge = stripe.Charge.create(
                    amount=total_cost*100, # amount in cents, again
                    currency="usd",
                    card=token,
                    description="{email}".format(email=request.user.email)
                )
                receipt.stripe_charge = charge.id
                receipt.paid = True

                for reg in receipt.regs:
                    reg.paid = True
                    reg.amount_paid = reg.due
                    reg.save()
                    
            except stripe.CardError as inst:
                receipt.problem = str(inst)


        receipt.total = total_cost
        receipt.save()


    return HttpResponseRedirect(reverse('event_registration_complete', kwargs={'pk': receipt.pk}))

@login_required
def event_reg_complete(request, pk=None):
    receipt = get_object_or_404(Receipt, pk=pk)

    return render_to_response('events/events_reg_complete.html', {'receipt': receipt}, context_instance=RequestContext(request))

@login_required
def event_admin_list(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden('')

    events = EventInfo.objects.all().order_by('-event_start')
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    return render_to_response('events/admin/events_list.html', 
                            {'events': events, 'today':datetime.date(now.year, now.month, now.day) }, 
                            context_instance=RequestContext(request))

@login_required
def event_admin_view(request, pk):
    event = get_object_or_404(EventInfo, pk=pk)

    if not request.user.is_superuser:
        return HttpResponseForbidden('only admins can see this report.')

    regs = event.eventregistration_set.all().exclude(option__npc=True).order_by('option__name')
    crunchies = event.eventregistration_set.filter(option__npc=True)
    reportcards = event.eventregistration_set.filter(reportcard_submitted=True).order_by('reportcard__submitted', 'user__first_name')

    factions = []
    faction_list = Faction.objects.all()
    for faction in faction_list:
        charsforfaction = FactionStatus.objects.filter(member=True,faction=faction).values_list('char', flat=True)
        

        factions.append({'name': faction.name,
         'count': regs.filter(char__in=charsforfaction).count(),
         'new': regs.filter(char__in=charsforfaction).filter(new_char=True).count(),
         })

    headers = []
    header_list = Header.objects.all()
    for header in header_list:
        charsforheader = header.character_set.all()
        

        headers.append({'name': header.name,
         'count': regs.filter(char__in=charsforheader).count(),
         })

    professions = []
    profession_list = Profession.objects.all()
    for profession in profession_list:
        charsforprof = ProfessionBought.objects.filter(profession=profession).values_list('char', flat=True)
        

        professions.append({'name': profession.name,
         'count': regs.filter(char__in=charsforprof).count(),
         })

    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    return render_to_response('events/admin/events_view.html', 
                            {'event': event, 
                            'today':datetime.date(now.year, now.month, now.day),
                            'regs': regs,
                            'crunchies': crunchies,
                            'reportcards': reportcards,
                            'factions':factions,
                            'headers': headers,
                            'professions': professions,
                             }, 
                            context_instance=RequestContext(request))


@login_required
def event_new_players(request, event):
    if not request.user.is_superuser:
        return HttpResponseForbidden('only admins can see this report.')

    event = get_object_or_404(EventInfo, pk=event)
    regs = event.eventregistration_set.filter(char__is_new=True).exclude(option__npc=True)

    return render_to_response('events/admin/events_new_players.html', 
                            {'event': event, 
                            'regs':regs,
                             }, 
                            context_instance=RequestContext(request))


@login_required
def event_cabins(request, event):
    if not request.user.is_superuser:
        return HttpResponseForbidden('only admins can see this report.')

    event = get_object_or_404(EventInfo, pk=event)

    if request.method == 'GET':
        regs = []

        options = event.registrationoptions_set.all()
        for option in options:
            eventregs = event.eventregistration_set.filter(option=option)
            slots=[]
            for x in range(0,option.assignments+1):
                slots.append({'num': x, 'players': eventregs.filter(cabin_num=x)})
            regs.append({'option': option,
                            'slots': slots })


        return render_to_response('events/admin/events_cabins.html', 
                                {'event': event,
                                 'regs': regs },
                                context_instance=RequestContext(request))

    assignments = json.loads(request.POST['assignments'])
    for assign in assignments:
        for reg in assign['players']:
            event.eventregistration_set.filter(pk=reg).update(cabin_num=assign['cabin_num'])

    return HttpResponse('')


@login_required
def event_report_card(request, pk):
    reg = get_object_or_404(EventRegistration, pk=pk)
    (card, created) = ReportCard.objects.get_or_create(reg=reg)

    if reg.reportcard_submitted:
        return HttpResponseRedirect('/')

    if request.user != reg.user:
        return HttpResponseRedirect('/')

    if request.method == 'GET':
        return render_to_response('events/events_report_card.html', {'reg': reg, 'card': card}, context_instance=RequestContext(request))


    reg.reportcard_submitted = True
    reg.save()
    

    card.enjoy_yourself = request.POST.get('enjoy_yourself',0)
    card.likely_to_return = request.POST.get('likely_to_return',0)
    card.rules = request.POST['rules']
    card.food = request.POST['food']
    card.puzzles = request.POST['puzzles']
    card.role_playing = request.POST['role_playing']
    card.costumes = request.POST['costumes']
    card.overall = request.POST['overall']
    card.anyone_help = request.POST['anyone_help']
    card.plots = request.POST['plots']
    card.goals = request.POST['goals']
    card.comments = request.POST['comments']


    card.save()

    return render_to_response('events/events_report_card_complete.html', {'reg': reg, 'card': card}, context_instance=RequestContext(request))

@login_required
def event_report_card_admin_view(request, event, pk):
    if not request.user.is_superuser:
        return HttpResponseForbidden('only admins can see this report.')

    reg = get_object_or_404(EventRegistration, pk=pk)
    card = reg.reportcard

    return render_to_response('events/admin/events_report_card.html', {'reg': reg, 'card': card}, context_instance=RequestContext(request))

@login_required
def event_report_card_pdf(request, event):
    event = get_object_or_404(EventInfo, pk=event)

    if not request.user.is_superuser:
        return HttpResponseForbidden('only admins can see this report.')

    regs = event.eventregistration_set.all().order_by('user__first_name', 'user__last_name')
    reportcards = ReportCard.objects.filter(reg__event=event, reg__reportcard_submitted=True)
    ratings = {}

    perc_returned = ( reportcards.count() * 1.0 / regs.exclude(option__npc=True).count() ) * 100

    ratings['returned'] = {'yes':perc_returned, 'no': 100 - perc_returned }


    ratings['enjoy_yourself'] = {'yes':( reportcards.filter(enjoy_yourself=True).count() * 1.0 / reportcards.count() * 1.0 ) * 100,
                                    'no':( reportcards.filter(enjoy_yourself=False).count() * 1.0 / reportcards.count() * 1.0 ) * 100 }

    ratings['likely_to_return'] = {'yes':( reportcards.filter(likely_to_return=True).count() * 1.0 / reportcards.count() * 1.0 ) * 100,
                                    'no':( reportcards.filter(likely_to_return=False).count() * 1.0 / reportcards.count() * 1.0 ) * 100 }

    ratings['overall'] = reportcards.annotate(avg=Avg('overall'))[0].avg

    outfile = StringIO.StringIO()
    html = render_to_string('events/admin/events_report_card_pdf.html', {'event': event, 'regs': regs, 'ratings': ratings, }, context_instance=RequestContext(request))

    pdf = xhtml2pdf.CreatePDF(html,outfile, path=settings.STATIC_ROOT, show_error_as_pdf=True)

    response = HttpResponse(outfile.getvalue(), mimetype='application/pdf')
    response['Content-Disposition'] = 'filename="Report cards for {eventname}.pdf'.format(eventname=str(event))
    return response


