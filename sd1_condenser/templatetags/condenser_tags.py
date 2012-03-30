from django import template

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
