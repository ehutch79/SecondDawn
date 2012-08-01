from django.conf.urls.defaults import patterns, include, url
from tastypie.api import Api

from sd1_condenser import api

v1_api = Api(api_name='v1')
v1_api.register(api.CharacterResource())
v1_api.register(api.SkillResource())
#v1_api.register(api.HeaderResource())
#v1_api.register(api.FactionResource())
v1_api.register(api.ProfessionResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'seconddawn.views.home', name='home'),
    # url(r'^seconddawn/', include('seconddawn.foo.urls')),

    url(r'^player/list/$', 'sd1_condenser.views.player_list', name='condenser_player_list'),
    url(r'^player/(?P<slug>[-\w\d]+)/give_eeps/$', 'sd1_condenser.views.player_grant_eeps', name='condenser_player_grant_eeps'),
    url(r'^player/(?P<slug>[-\w\d]+)/staff_view/$', 'sd1_condenser.views.player_staff_view', name='condenser_player_staff_view'),
    url(r'^player/(?P<slug>[-\w\d]+)/events/$', 'sd1_condenser.views.player_upcoming_events', name='condenser_player_events'),
    

    url(r'^char/create/$', 'sd1_condenser.views.character_create', name='condenser_char_create'),

    url(r'^char/view/(?P<slug>[-\w\d]+)/attr/$', 'sd1_condenser.views.character_adjust_attributes', name='condenser_char_attr_adjust'),
    url(r'^char/view/(?P<slug>[-\w\d]+)/reset/$', 'sd1_condenser.views.character_reset', name='condenser_char_reset'),
    url(r'^char/view/(?P<slug>[-\w\d]+)/buy_build/$', 'sd1_condenser.views.char_buy_build', name='condenser_char_buy_build'),
    url(r'^char/view/(?P<slug>[-\w\d]+)/approve_bg/$', 'sd1_condenser.views.char_approve_bg', name='condenser_char_approve_bg'),
    
    url(r'^char/view/(?P<slug>[-\w\d]+)/sheet/$', 'sd1_condenser.views.character_sheet', name='condenser_char_sheet'),
    url(r'^char/view/(?P<slug>[-\w\d]+)/$', 'sd1_condenser.views.character_view', name='condenser_char_view'),
    url(r'^char/sheets/(?P<event>[-\w\d]+)/$', 'sd1_condenser.views.character_sheet_pdf', name='condenser_char_sheets_pdf'),

    url(r'^char/delete/(?P<slug>[-\w\d]+)/$', 'sd1_condenser.views.char_delete', name='condenser_char_delete'),


    url(r'^char/api/', include(v1_api.urls)),
    url(r'^$', 'sd1_condenser.views.character_view', name='condenser_char_home'),
    
)
