import uuid
from datetime import datetime
from akismet import Akismet

from django.views.generic import View, RedirectView, DetailView, ListView, CreateView, UpdateView, FormView, TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.utils import simplejson as json
from django.http import HttpResponse, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404
from django.contrib.auth import authenticate, login
from django.contrib import messages

from django_neve.models import Profile, ActivityLog, SocialNetworkLink

from django_neve.forms import CreateAccountForm, PasswordResetEmailForm, PasswordResetForm
#from django_neve.models import PasswordReset
from django_neve.forms import LoginForm as AuthenticationForm
from django_neve.forms import RegisterForm, ProfileEditForm

import urlparse

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, QueryDict
from django.template.response import TemplateResponse
from django.utils.http import base36_to_int
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site

from django.conf import settings
AKISMET_KEY = getattr(settings, 'AKISMET_KEY', False)

import logging
logger = logging.getLogger(__name__)


# class PasswordResetEmail(FormView):
#     template_name = 'django_neve/password_reset_email_form.html'
#     form_class = PasswordResetEmailForm
# 
#     def get_success_url(self):
#         return reverse('django_neve_password_reset_email_done')
# 
#     def post(self, request, *args, **kwargs):
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
# 
# 
# 
#         if form.is_valid():
#             contact_email = form.cleaned_data['contact_email']
#             self.contact_email = contact_email
#             emails = User._default_manager.filter(email__iexact=contact_email)
# 
#             if emails.count():
#                 return self.form_valid(form)
#             else:
#                 form._errors["contact_email"] = form.error_class([u'Please double check your email'])
#                 return self.form_invalid(form)
#         else:
#             form._errors["contact_email"] = form.error_class([u'Please double check your email'])
#             return self.form_invalid(form)
# 
# 
# 
#     def form_valid(self, form):
#         contact_email = form.cleaned_data['contact_email']
#         self.contact_email = contact_email
#         emails = User._default_manager.filter(email__iexact=contact_email)
# 
#         for email in emails:
#             reset = PasswordReset()
#             reset.user = email
#             reset.email = contact_email
#             reset.requested_ip = self.request.META['REMOTE_ADDR']
#             reset.save()
#             reset.send()
# 
#         return super(PasswordResetEmail, self).form_valid(form)
# 
# class PasswordResetEmailSuccess(TemplateView):
#     template_name = 'django_neve/password_reset_email_success.html'
# 
# 
# class PasswordResetView(FormView, SingleObjectMixin):
#     template_name = 'django_neve/password_reset_form.html'
#     form_class = PasswordResetForm
#     model = PasswordReset
# 
# 
#     def get_form(self, form_class):
#         self.object = self.get_object()
#         if self.object.expires < datetime.utcnow():
#             self.object.delete()
#             raise Http404
# 
#         result = form_class(self.object.user, **self.get_form_kwargs())
# 
#         return result
# 
#     def get_success_url(self):
#         return reverse('django_neve_login')
# 
# 
#     def form_valid(self, form):
#         form.save()
#         self.object.delete()
# 
#         return super(PasswordResetView, self).form_valid(form)
# 
def gen_username():
    username = list(str(uuid.uuid4()))
    username.pop(23)
    username.pop(19)
    username.pop(18)
    username.pop(14)
    username.pop(13)
    username.pop(8)
    username = ''.join(username)

    return username

@csrf_protect
@never_cache
def register_view(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('django_neve_profile_edit', kwargs={'slug': request.user.get_profile().slug}))

    if request.method == "GET":
        form = RegisterForm()
        return TemplateResponse(request, 'django_neve/register.html', {'form': form})
    
    if request.method == "POST":
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            user = User()
            
            ## set username to a random unique string
            username = gen_username()
            #ensure there is no collision
            while User._default_manager.filter(username=username).count() > 0:
                username = gen_username()
            
            user.username = username
            user.email = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password'])
            
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
    
            user.is_active = True
            user.save()
            
            if AKISMET_KEY:
                akismet = Akismet(agent='django/1.3')
                akismet.key = AKISMET_KEY
                akismet.blog_url = "http://{host}/".format(host=request.META['HTTP_HOST'])
                if not akismet.verify_key():
                    log = ActivityLog()
                    log.ip = request.META['REMOTE_ADDR']
                    log.user = user
                    log.user_agent = request.META['HTTP_USER_AGENT']
                    log.type='alert'
                    log.action = 'Registration: Akistmet key not valid'
                    log.save()
                    
                spam = akismet.comment_check(None, {
                    'user_ip': request.META['REMOTE_ADDR'],
                    'user_agent': request.META['HTTP_USER_AGENT'],
                    'referrer': request.META['HTTP_REFERER'],
                    'comment_type': 'registration',
                    'comment_author_email': user.email,
                    'comment_author': '{first_name} {last_name}'.format(first_name=user.first_name, last_name=user.last_name),
                    }, build_data=False)
                
                if spam:
                    log = ActivityLog()
                    log.ip = request.META['REMOTE_ADDR']
                    log.user = user
                    log.user_agent = request.META['HTTP_USER_AGENT']
                    log.type='alert'
                    log.action = 'Registration: Akismet reported as potential spammer'
                    log.save()

                    user.is_active = False
                    
            if 'HTTP_CF_IPCOUNTRY' in request.META:
                if request.META['HTTP_CF_IPCOUNTRY'] not in ('US', 'MX', 'CA',):
                    log = ActivityLog()
                    log.ip = request.META['REMOTE_ADDR']
                    log.user = user
                    log.user_agent = request.META['HTTP_USER_AGENT']
                    log.type='alert'
                    log.action = 'Registration: International registration'
                    log.save()

                    user.is_active = False
            
            user.save()
            
            log = ActivityLog()
            log.ip = request.META['REMOTE_ADDR']
            log.user = user
            log.user_agent = request.META['HTTP_USER_AGENT']
            log.type='info'
            log.action = 'Registration: User Created'
            log.save()
            
            profile = user.get_profile()
            profile.display_name = form.cleaned_data['display_name']
            profile.save()
            
            if user.is_active:
                login(request, authenticate(username=user.email, password=form.cleaned_data['password']))
                return HttpResponseRedirect(reverse('django_neve_profile_edit', kwargs={'slug': profile.slug}))
            else:
                return HttpResponseRedirect('/')
            
        else:
            ### form not valid
            return TemplateResponse(request, 'django_neve/register.html', {'form': form})


    
    log = ActivityLog()
    log.ip = request.META['REMOTE_ADDR']
    log.user_agent = request.META['HTTP_USER_AGENT']
    log.type='alert'
    log.action = 'Registration: Bad Method'
    log.save()
    
    response = HttpResponse("Error: Method not allowed")
    response.status_code=405
    return response

@csrf_protect
@never_cache
def login_view(request, template_name='django_neve/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.REQUEST.get(redirect_field_name, '')

    if request.method == "POST":
        form = authentication_form(data=request.POST)
        if form.is_valid():
            netloc = urlparse.urlparse(redirect_to)[1]

            # Use default setting if redirect_to is empty
            if not redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Heavier security check -- don't allow redirection to a different
            # host.
            elif netloc and netloc != request.get_host():
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Okay, security checks complete. Log the user in.
            auth_login(request, form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)

    request.session.set_test_cookie()

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


@csrf_protect
@never_cache
@login_required
def profile_edit_view(request, slug=None):    
    user_profile = request.user.get_profile()
    if not slug or (not request.user.is_superuser and user_profile.slug != slug):
        return HttpResponseRedirect(reverse('django_neve_profile_edit', kwargs={'slug': user_profile.slug}))
        
    profile = get_object_or_404(Profile, slug=slug)
    user = profile.user

    template_name = 'django_neve/profile_edit_full.html'
    if request.is_ajax():
        template_name = 'django_neve/profile_edit.html'
 
    if request.method == "GET":
        if not request.is_ajax():
            try:
                medic = user.personalprofile
            except:
                messages.warning(request, 'Medical / Allergy profile missing.')

        
        form = ProfileEditForm(initial={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'display_name': profile.display_name,
                'email': user.email,
                'user_id': user.username,
            })
                
        return render_to_response(template_name, {'form': form, 'slug': profile.slug }, context_instance=RequestContext(request))
    
    if request.method == "POST":
        form = ProfileEditForm(request.POST)
        if form.is_valid():
        
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()

            profile = user.get_profile()
            profile.display_name = form.cleaned_data['display_name']
            profile.save()
            saved = False

            messages.success(request, 'Profile details updated.')

            return HttpResponseRedirect(reverse('django_neve_profile_edit', kwargs={'slug': profile.slug}) )
  
        return render_to_response(template_name, {'form': form, 'slug': profile.slug }, context_instance=RequestContext(request))
    
    
    
    log = ActivityLog()
    log.ip = request.META['REMOTE_ADDR']
    log.user_agent = request.META['HTTP_USER_AGENT']
    log.type='alert'
    log.user = request.user
    log.action = 'Edit profile: Bad Method'
    log.save()
    
    response = HttpResponse("Error: Method not allowed")
    response.status_code=405
    return response
