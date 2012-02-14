import math

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
from django.db.models import F, Q

import stripe

from sd1_events.models import *

import logging

logger = logging.getLogger(__name__)


def event_list(request):
    events = EventInfo.objects.all()
    reged_events = EventRegistration.objects.filter(user=request.user).values_list('event__pk',flat=True)

    return render_to_response('events/events_list.html', {'events': events, 'reged_events': reged_events}, context_instance=RequestContext(request))

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

def event_reg_complete(request, pk=None):
    receipt = get_object_or_404(Receipt, pk=pk)

    return render_to_response('events/events_reg_complete.html', {'receipt': receipt}, context_instance=RequestContext(request))