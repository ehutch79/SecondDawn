import math
import datetime

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

from sd1_condenser.models import *
from sd1_condenser.forms import CreateCharacterForm

from sd1_events.models import EventInfo

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
        
    char.save()

    profession_list = dict([(k[-37:-1], v) for k, v in request.POST.items() if k[:11] == 'professions'])
    has_list = []
    print profession_list

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
        if profession_id not in has_list and num_profs < 3:
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
    reason = request.POST.get('eeps', '')

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

    return HttpResponse('saved')


@login_required
def char_delete(request, slug):
    char = get_object_or_404(Character, slug=slug)

    now = datetime.datetime.now()

    if request.user != char.user or not char.is_new:
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

    if request.method != 'POST':
        return HttpResponseForbidden('method not allowed')

    if request.user != char.user and not request.user.is_superuser:
        return HttpResponseForbidden('You may only buy build on your own character')
    
    build_events = EventInfo.objects.filter(build_blackout_start__lte=now, event_end__gte=now)
    if build_events.count() > 0:
        return HttpResponseForbidden('You may not buy build during a build blackout')

    if not char.can_buy_build:
        return HttpResponseForbidden('You have already bought build for this character')

    to_buy = request.POST.get('build_to_buy', 0)
    if to_buy > 12:
        to_buy = 12
    temp = to_buy
    cost = 0
    if temp < 9:
        cost = temp * 100
    else:
        cost = 800
        temp -= 8
        add_cost = 100
        while temp:
            add_cost += 100
            temp -= 1
            cost += add_cost


    if cost <= char.user.eepsbank.eeps:
        eeps = char.user.eepsbank
        chars.update(can_buy_build=False)
        chars.update(free_build=F('free_build')+to_buy)
        eeps -= cost
        eeps.save()

    return HttpResponseRedirect(reverse('condenser_char_view', kwargs={'slug': chars[0].slug}))

