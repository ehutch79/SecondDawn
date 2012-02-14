from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'seconddawn.views.home', name='home'),
    # url(r'^seconddawn/', include('seconddawn.foo.urls')),

#    url(r'^player/list/$', 'sd1_condenser.views.player_list', name='condenser_player_list'),
#    url(r'^player/(?P<slug>[-\w\d]+)/give_eeps/$', 'sd1_condenser.views.player_grant_eeps', name='condenser_player_grant_eeps'),
    url(r'^register/$', 'sd1_events.views.register_for_events', name='register_for_events'),
    url(r'^register/complete/(?P<pk>[-\w\d]+)/$', 'sd1_events.views.event_reg_complete', name='event_registration_complete'),
    
    url(r'^$', 'sd1_events.views.event_list', name='event_list'),
    
)
