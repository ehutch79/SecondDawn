from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'seconddawn.views.home', name='home'),
    # url(r'^seconddawn/', include('seconddawn.foo.urls')),

#    url(r'^player/list/$', 'sd1_condenser.views.player_list', name='condenser_player_list'),
#    url(r'^player/(?P<slug>[-\w\d]+)/give_eeps/$', 'sd1_condenser.views.player_grant_eeps', name='condenser_player_grant_eeps'),
    url(r'^register/$', 'sd1_events.views.register_for_events', name='register_for_events'),
    url(r'^register/(?P<pk>[-\w\d]+)/complete/$', 'sd1_events.views.event_reg_complete', name='event_registration_complete'),
    url(r'^register/(?P<pk>[-\w\d]+)/report-card/$', 'sd1_events.views.event_report_card', name='event_report_card'),


    url(r'^list/$', 'sd1_events.views.event_admin_list', name='event_admin_list'),
    url(r'^(?P<event>[-\w\d]+)/cabins/$', 'sd1_events.views.event_cabins', name='event_cabins'),
    url(r'^(?P<event>[-\w\d]+)/player/(?P<reg>[-\w\d]+)/$', 'sd1_events.views.event_player', name='event_player'),
    url(r'^(?P<event>[-\w\d]+)/new_players/$', 'sd1_events.views.event_new_players', name='event_new_players'),
    url(r'^(?P<event>[-\w\d]+)/report-card/pdf/$', 'sd1_events.views.event_report_card_pdf', name='event_report_card_admin_view_pdf'),
    url(r'^(?P<event>[-\w\d]+)/report-card/(?P<pk>[-\w\d]+)/$', 'sd1_events.views.event_report_card_admin_view', name='event_report_card_admin_view'),
    url(r'^(?P<pk>[-\w\d]+)/$', 'sd1_events.views.event_admin_view', name='event_admin_view'),



    url(r'^$', 'sd1_events.views.event_list', name='event_list'),
    
)
