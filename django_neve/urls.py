from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'seconddawn.views.home', name='home'),
    # url(r'^seconddawn/', include('seconddawn.foo.urls')),

    url(r'^login/$', 'django_neve.views.login_view', name='django_neve_login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='django_neve_logout'),
    url(r'^register/$', 'django_neve.views.register_view', name='django_neve_register'),
    url(r'^activate/(?P<pk>[-\w\d]+)/$', 'django_neve.views.user_activate', name='django_neve_activate_user'),

    url(r'^edit/(?P<slug>[-\w\d]+)/$', 'django_neve.views.profile_edit_view', name='django_neve_profile_edit'),
)
