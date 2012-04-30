from django import template
from django.utils.timezone import utc

import datetime

from sd1_condenser.models import *


register = template.Library()

def get_faction_list(parser, token):
    return GetFactionsNode()

class GetFactionsNode(template.Node):
    def __init__(self):
        pass

    def render(self, context):
        context['factions_list'] = Faction.objects.all()
        return ''

register.tag('get_faction_list', get_faction_list)


def get_npc_list(parser, token):
    return GetNPCNode()

class GetNPCNode(template.Node):
    def __init__(self):
        pass

    def render(self, context):
        context['npc_list'] = Character.objects.filter(is_npc=True)
        return ''

register.tag('get_npc_list', get_npc_list)

def get_profession_list(parser, token):
    return GetProfNode()

class GetProfNode(template.Node):
    def __init__(self):
        pass

    def render(self, context):
        context['professions_list'] = Profession.objects.all()
        return ''

register.tag('get_profession_list', get_profession_list)


def get_headers_list(parser, token):
    return GetHeadersNode()

class GetHeadersNode(template.Node):
    def __init__(self):
        pass

    def render(self, context):
        context['headers_list'] = Header.objects.all()
        return ''

register.tag('get_headers_list', get_headers_list)

def get_reportcard_list(parser, token):
    return GetReportCardListNode()

class GetReportCardListNode(template.Node):
    def __init__(self):
        pass

    def render(self, context):
        user = template.Variable('user').resolve(context)
        now = datetime.datetime.utcnow().replace(tzinfo=utc)

        reportcards = user.eventregistration_set.filter(reportcard_submitted=False, event__event_start__lte=now)
        
        context['missing_reportcards'] = reportcards

        return ''

register.tag('get_reportcard_list', get_reportcard_list)
