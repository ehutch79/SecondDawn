from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'seconddawn.views.home', name='home'),
    # url(r'^seconddawn/', include('seconddawn.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('django_neve.urls')),
    url(r'^condenser/', include('sd1_condenser.urls')),
    url(r'^events/', include('sd1_events.urls')),

    (r'^$', login_required(TemplateView.as_view(template_name="base.html"))),
)



urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^/static/(?P<path>.*)$', 'serve'),
    )