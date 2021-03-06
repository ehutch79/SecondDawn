import math
import datetime
import StringIO

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
from django.utils.timezone import utc

import xhtml2pdf.pisa as xhtml2pdf


from sd1_condenser.models import *
from sd1_condenser.forms import CreateCharacterForm

from sd1_events.models import *

import logging

logger = logging.getLogger(__name__)


@login_required
def character_view(request, slug=None):
    template_name = 'condenser/char_view_full.html'
    if request.is_ajax():
        template_name = 'condenser/char_view.html'

    if slug:
        char = get_object_or_404(Character, slug=slug)
    else:
        char = None

        chars = Character._default_manager.filter(user=request.user).exclude(is_deceased=True).exclude(is_retired=True)
        if chars.count() > 0:
            char = chars[0]

        if not char:
            if not request.user.is_staff and not request.user.is_superuser:
                return HttpResponseRedirect(reverse('condenser_char_create'))
            else: 
                return HttpResponseRedirect(reverse('condenser_char_create'))

    if not request.user.is_staff and not request.user.is_superuser and request.user != char.user:
        return HttpResponseForbidden('You may only view your own character')

    return render_to_response(template_name, {'char': char, 'slug': slug}, context_instance=RequestContext(request))

@login_required
def character_sheet(request, slug=None):
    template_name = 'condenser/char_sheet_fame.html'
    
    char = get_object_or_404(Character, slug=slug)

    if not request.user.is_staff and not request.user.is_superuser and request.user != char.user:
        return HttpResponseForbidden('You may only view your own character')

    return render_to_response(template_name, {'char': char, 'slug': slug}, context_instance=RequestContext(request))



@login_required
def character_sheet_pdf(request, event):
    template_name = 'condenser/char_sheet_multiple.html'
    
    event = get_object_or_404(EventInfo, pk=event)
    chars = []
#    chars = Character.objects.all().order_by('slug')
    for reg in event.eventregistration_set.all().order_by('char__slug'):
        if reg.char:
            chars.append(reg.char)

    if not request.user.is_staff and not request.user.is_superuser:
        return HttpResponseForbidden('You may only view your own character')

    return render_to_response(template_name, {'chars': chars }, context_instance=RequestContext(request))

    outfile = StringIO.StringIO()
    pdf = xhtml2pdf.CreatePDF(html,outfile, show_error_as_pdf=True)

    response = HttpResponse(outfile.getvalue(), mimetype='application/pdf')
    response['Content-Disposition'] = 'filename="Char Sheets for {eventname}.pdf'.format(eventname=str(event))
    return response

@login_required
def character_create(request):
    template_name = 'condenser/char_create_full.html'
    if request.is_ajax():
        template_name = 'condenser/char_create.html'

    form = CreateCharacterForm()

    if request.method == "GET":
        return render_to_response(template_name, {'form': form}, context_instance=RequestContext(request))

    if request.method == "POST":
        form = CreateCharacterForm(request.POST)

        if form.is_valid():
            char = Character()
            char.name = form.cleaned_data['name']
            char.user = request.user

            if request.user.is_superuser or request.user.is_staff:
                char.free_build = 999
                char.is_new = False
                char.is_npc = True
            char.save()

            header = Header.objects.get(pk=form.cleaned_data['header'])
            char.headers.add(header)

            faction_member = FactionStatus()
            faction_member.faction = Faction.objects.get(pk=form.cleaned_data['faction'])
            faction_member.char=char
            faction_member.member=True
            faction_member.rep = 25
            faction_member.save();

            return HttpResponseRedirect(reverse('condenser_char_view', kwargs={'slug': char.slug}))

        return render_to_response(template_name, {'form': form}, context_instance=RequestContext(request))


def calculate_cost(current, end):
    start = int(current) + 1
    end = int(end)
    if end <= current:
        return 0
    if start == end:
        return end

    term = (end - current)
    factor = term / float(2)
    base = (2 * start) + (term - 1)
    return int(factor * base)


@login_required
def character_reset(request, slug):
    return False
    
    char = get_object_or_404(Character, slug=slug)
    template_name = 'condenser/char_view_attr.html'

    if char.user != request.user and not request.user.is_superuser:
        return HttpResponseForbidden('You may only edit your own character')

#    if request.method != "POST":
#        return HttpResponseRedirect(reverse('condenser_char_view', kwargs={'slug': char.slug}))
    char.free_build = char.free_build + char.build_spent
    
    char.build_spent = 0
    char.is_new = False
    char.is_updated = True
    
    char.blood = 1
    char.might = 1
    char.mind  = 1
    char.finesse = 1
    char.will  = 1

    char.save()

    for skill in char.skills.all():
        skill.delete()

    for prof in char.professions.all():
        prof.delete()

    if not request.is_ajax():
        return HttpResponseRedirect(reverse('condenser_char_view', kwargs={'slug': char.slug}))

    success = "Your attributes were updated"
    return HttpResponse(success)

@login_required
def character_adjust_attributes(request, slug):
    char = get_object_or_404(Character, slug=slug)
    template_name = 'condenser/char_view_attr.html'

    if char.user != request.user and not request.user.is_superuser:
        return HttpResponseForbidden('You may only edit your own character')

    if request.method != "POST":
        return HttpResponseRedirect(reverse('condenser_char_view', kwargs={'slug': char.slug}))

    blood = int(request.POST.get('blood', '0'))
    might = int(request.POST.get('might', '0'))
    mind = int(request.POST.get('mind', '0'))
    finesse = int(request.POST.get('finesse', '0'))
    will = int(request.POST.get('will', '0'))

    new_cost = 0

    new_cost += calculate_cost(char.blood, char.blood + blood)
    new_cost += calculate_cost(char.might, char.might + might)
    new_cost += calculate_cost(char.mind, char.mind + mind)
    new_cost += calculate_cost(char.finesse, char.finesse + finesse)
    new_cost += calculate_cost(char.will, char.will + will)

    if new_cost > char.free_build:
        if not request.is_ajax():
            messages.error(request, 'You\'ve tried to spend more build then you have somehow!')
            return HttpResponseRedirect(reverse('condenser_char_view', kwargs={'slug': char.slug}))

        error = "You've tried to spend more build then you have somehow!"
        return render_to_response(template_name, {'char': char, 'attr_error': error},
                                  context_instance=RequestContext(request))

    char.free_build -= new_cost
    char.build_spent += new_cost

    char.blood += blood
    char.might += might
    char.mind += mind
    char.finesse += finesse
    char.will += will
    if not char.background_approved:
        char.background = request.POST.get('background', '')
    if request.POST.get('background_approved', False):
        char.background_approved = True
        char.free_build += 5
    char.save()

    skill_list = request.POST.getlist('skills[]')

    has_list = []
    has_skills = char.skills.all()
    for skillbought in has_skills:
        if skillbought.skill.pk not in skill_list and ( request.user.is_superuser or request.user.is_staff):
            skillbought.delete()
            char.free_build += skillbought.paid_total
            char.build_spent -= skillbought.paid_total
        else:
            has_list.append(skillbought.skill.pk)
    
    for skill_id in skill_list:
        if skill_id not in has_list:
            skill = Skill.objects.get(pk=skill_id)
            buy = SkillBought()
            buy.skill = skill
            buy.char = char
            buy.paid_total = skill.build_cost
            buy.save()
            has_list.append(skill.pk)

            char.free_build -= skill.build_cost
            char.build_spent += skill.build_cost
            
            if skill.grants.all().count():
                for granted in skill.grants.all():
                    buy = SkillBought()
                    buy.skill = granted
                    buy.char = char
                    buy.paid_total = 0
                    buy.bundled_from = skill
                    buy.save()
                    has_list.append(granted.pk)
    
    if not char.is_npc:
        char.is_updated = True
    char.save()

    profession_list = dict([(k[-37:-1], v) for k, v in request.POST.items() if k[:11] == 'professions'])
    has_list = []
    

    for professionbought in char.professions.all():
        if professionbought.profession.pk not in profession_list and ( request.user.is_superuser or request.user.is_staff):
            cost = professionbought.calc_cost_to(5, professionbought.score)
            cost += char.professions.all().count() * 3
            
            char.free_build += cost
            char.build_spent -= cost                        

            professionbought.delete()
        else:
            has_list.append(professionbought.profession.pk)

    char.save()

    for profession_id in profession_list:
        profession_score = int(profession_list[profession_id])
        num_profs = int(char.professions.all().count()+1)
        if profession_id not in has_list and (num_profs < 4 or request.user.is_superuser or request.user.is_staff):
            profession = Profession.objects.get(pk=profession_id)
            buy = ProfessionBought()
            buy.profession = profession
            buy.char = char
            build_cost = buy.calc_cost_to(buy.score, profession_score) + ( num_profs * 3)
            buy.score = profession_score
            buy.save()
            has_list.append(profession.pk)
            char.free_build -= build_cost
            char.build_spent += build_cost
        else:
            buy = ProfessionBought.objects.get(char=char, profession=profession_id)
            if(profession_score > buy.score):
                build_cost = buy.calc_cost_to(buy.score, profession_score)
                char.free_build -= build_cost
                char.build_spent += build_cost
                buy.score = profession_score
                buy.save()
            
            
    char.save()

    if not request.is_ajax():
        return HttpResponseRedirect(reverse('condenser_char_view', kwargs={'slug': char.slug}))

    success = "Your attributes were updated"
    return HttpResponse(success)


@login_required
def player_list(request):
    template_name = 'condenser/player/list.html'
    if not request.user.is_superuser:
        return HttpResponseForbidden('only admins may see this page')

    players = User.objects.filter(is_active=True)
    for player in players:
        try: 
            prof = player.personalprofile
        except:
            prof = PersonalProfile()
            prof.user = player
            prof.save()

    return render_to_response(template_name, { 'players': players },
                              context_instance=RequestContext(request))


@login_required
def player_grant_eeps(request, slug):
    player = get_object_or_404(User, username=slug)
    template_name = 'condenser/char_view_attr.html'

    if not request.user.is_superuser:
        return HttpResponseForbidden('only senior staff may grant xp')

    if request.method != "POST":
        return HttpResponseForbidden('method not allowed')

    eeps = int(request.POST.get('eeps', '0'))
    reason = request.POST.get('reason', '')

    try:
        eeps_bank = player.eepsbank
    except:
        eeps_bank = EepsBank()
        eeps_bank.user = player
        eeps_bank.save()

    EepsBank.objects.filter(pk=eeps_bank.pk).update(eeps=F('eeps')+eeps)

    eeps_record = EepsRecord()
    eeps_record.user = player
    eeps_record.eeps = eeps
    eeps_record.reason = reason
    eeps_record.save()
    player = User.objects.get(pk=player.pk)

    return HttpResponse(json.dumps({'eeps': player.eepsbank.eeps, 'pk': player.pk }), mimetype="application/json")


@login_required
def player_staff_view(request, slug=None):
    template_name = 'condenser/player/staff_view_full.html'

    if not request.user.is_staff and not request.user.is_superuser:
        return HttpResponseForbidden('Staff only, sorry')
    
    user = get_object_or_404(User, username=slug)
    
    all_eeps = EepsRecord.objects.all()
    
    return render_to_response(template_name, {'player': user, 'records': all_eeps}, context_instance=RequestContext(request))

 

@login_required
def char_delete(request, slug):
    char = get_object_or_404(Character, slug=slug)

    now = datetime.datetime.now()

    if ( request.user != char.user or not char.is_new ) and ( not request.user.is_superuser and not request.user.is_staff):
        return HttpResponseForbidden('You may only delete your own new characters')

    build_events = EventInfo.objects.filter(build_blackout_start__lte=now, event_end__gte=now)
    if build_events.count() > 0:
        return HttpResponseForbidden('You may not delete a character during a build blackout')

    char.delete()

    return HttpResponseRedirect(reverse('condenser_char_create'))

@login_required
def char_approve_bg(request, slug):
    chars = Character.objects.filter(slug=slug)

    if not request.user.is_staff and not request.user.is_superuser:
        return HttpResponseForbidden('only staff may approve backgrounds')

    chars.update(background_approved=True)
    chars.update(free_build=F('free_build')+5)
    if chars.count() > 0:
        return HttpResponseRedirect(reverse('condenser_char_view', kwargs={'slug': chars[0].slug}))
    else:
        return HttpResponseRedirect('/')


@login_required
def char_buy_build(request, slug):
    chars = Character.objects.filter(slug=slug)
    char = get_object_or_404(Character, slug=slug)

    now = datetime.datetime.now()


    if request.method != 'POST':
        return HttpResponseForbidden('method not allowed')

    if request.user != char.user and not request.user.is_superuser:
        return HttpResponseForbidden('You may only buy build on your own character')
    
    build_events = EventInfo.objects.filter(build_blackout_start__lte=now, event_end__gte=now)
    if build_events.count() > 0:
        return HttpResponseForbidden('You may not buy build during a build blackout')

    if not char.can_buy_build:
        return HttpResponseForbidden('You have already bought build for this character')

    to_buy = int(request.POST.get('to_buy', 0))
    if to_buy > 10:
        to_buy = 10
    temp = to_buy
    cost = 0
    # if temp < 9:
    #     cost = temp * 100
    # else:
    #     cost = 800
    #     temp -= 8
    #     add_cost = 100
    #     while temp:
    #         add_cost += 100
    #         temp -= 1
    #         cost += add_cost
    cost = temp * 100


    if cost <= char.user.eepsbank.eeps:
        eeps = char.user.eepsbank
        chars.update(can_buy_build=False)
        chars.update(free_build=F('free_build')+to_buy)
        eeps.eeps -= cost
        eeps.save()

        eeps_record = EepsRecord()
        eeps_record.user = char.user
        eeps_record.eeps = cost * -1
        eeps_record.reason = 'Bought Build for {name}'.format(name=char.name) 
        eeps_record.save()


        return HttpResponse('success buying {to_buy} build for {cost} xp'.format(to_buy=to_buy, cost=cost) )
    else:
        return HttpResponseForbidden('Failure buying {to_buy} build for {cost} xp, you only have {eeps} xp'.format(to_buy=to_buy, cost=cost, eeps=char.user.eepsbank.eeps) )

    #return HttpResponseRedirect(reverse('condenser_char_view', kwargs={'slug': chars[0].slug}))


@login_required
def player_upcoming_events(request, slug):
    player = get_object_or_404(User, username=slug)

    if request.method == 'GET':
        player_events = []
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        yesterday = now - datetime.timedelta(days=2)

        events = EventInfo.objects.filter(event_end__gte=yesterday)
        for event in events:
            player_reg = event.eventregistration_set.filter(user=player)

            reg_opt = None

            if player_reg.count():
                reg_opt = player_reg[0].option.pk


            element = {
                'name': str(event),
                'pk': event.pk,
                'options': [{'pk':option.pk, 'name':option.name} for option in event.registrationoptions_set.all() ],
                'set_as': reg_opt
            }
            player_events.append(element)

        return HttpResponse(json.dumps(player_events), mimetype="application/json");


    for item in request.POST:
        if item[0:5] != "event":
            continue
        
        pk = item[6:-1]
        event = EventInfo.objects.get(pk=pk)


        try:
            reg = EventRegistration.objects.get(event=event, user=player)
        except EventRegistration.DoesNotExist:
            reg = EventRegistration()
            reg.user = player
            reg.char = player.personalprofile.get_current_char()
            if not reg.char or reg.char.is_new:
                reg.new_char = True
            reg.event = event

        if not request.POST[item]:
            reg.delete()
            continue

        option = event.registrationoptions_set.filter(pk=request.POST[item])[0]

        reg.option = option
        reg.save()

    return HttpResponse('', mimetype="application/json");

@login_required
def label_form(request):
    template_name = 'condenser/labels/form.html'
    if not request.user.is_superuser:
        return HttpResponseForbidden('only admins may see this page')

    return render_to_response(template_name, { },
                              context_instance=RequestContext(request))


@login_required
def label_display(request):
    template_name = 'condenser/labels/display.html'
    if not request.user.is_superuser:
        return HttpResponseForbidden('only admins may see this page')

    item_name = request.GET.get('item-name', '')
    item_type = request.GET.get('item-type', '')
    item_effects = request.GET.get('item-effects', '')

    return render_to_response(template_name, { 'item_name': item_name,
                                                'item_type': item_type,
                                                'item_effects': item_effects,
                                                'total_range': range(0,16) },
                              context_instance=RequestContext(request))
