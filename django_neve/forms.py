from django import forms
from django.db import models
from django.contrib.auth.forms import SetPasswordForm, AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.validators import validate_email

from django_neve.models import Profile

class CreateAccountForm(forms.Form):
    contact_id = forms.CharField(widget=forms.HiddenInput)
    
    confirm = forms.BooleanField(required=True)
    

class PasswordResetEmailForm(forms.Form):
    contact_email = forms.EmailField()
    
class PasswordResetForm(SetPasswordForm):

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(_("The two password fields didn't match."))
        
        if len(password2) < 8:
            raise forms.ValidationError(_("You must have at least 8 characters in your password. Recommended is 12 at minimum"))
            
        return password2

class LoginForm(AuthenticationForm):
    username = forms.CharField(label=_("Email"), max_length=250)

class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    display_name = forms.CharField(required=False, max_length=75, help_text="What you'd like people to see publicly (We'll use your name if you leave this blank)")
    
    email = forms.CharField(max_length=250, help_text="For logging in and to contact you about account activity")

    password = forms.CharField(max_length=250, widget=forms.PasswordInput())
    confirm_password = forms.CharField(label="Confirm Pass", max_length=250, widget=forms.PasswordInput())
    
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if User._default_manager.filter(email=email).count():
            raise forms.ValidationError(_("This email has already been registered, perhaps you would like to reset your password"))

        validate_email(email)
        return email
                
                
    def clean_display_name(self):
        display_name = self.cleaned_data.get('display_name')

        if not display_name:
            display_name = '{first} {last}'.format(first=self.cleaned_data.get('first_name'), last=self.cleaned_data.get('last_name'))

        if Profile._default_manager.filter(display_name=display_name).count():
            raise forms.ValidationError(_("This public name has been taken already"))

        return display_name
        
        
        
    def clean_password(self):
        password2 = self.cleaned_data.get('password')
        if len(password2) < 8:
            raise forms.ValidationError(_("You must have at least 8 characters in your password. Recommended is 12 at minimum"))
        return password2    
    
    def clean_confirm_password(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirm_password')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(_("The two password fields didn't match."))
        
        return password2
        
class ProfileEditForm(forms.Form):
    user_id = forms.CharField(max_length=65, widget=forms.HiddenInput)
    
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    display_name = forms.CharField(required=False, max_length=75, help_text="What you'd like people to see publicly (We'll use your name if you leave this blank)")
    
    email = forms.CharField(max_length=250, help_text="For logging in and to contact you about account activity")
    
    def clean_display_name(self):
        display_name = self.cleaned_data.get('display_name')

        if not display_name:
            display_name = '{first} {last}'.format(first=self.cleaned_data.get('first_name'), last=self.cleaned_data.get('last_name'))

        if Profile._default_manager.filter(display_name=display_name).exclude(user__username=self.cleaned_data.get('user_id')).count():
            raise forms.ValidationError(_("This public name has been taken already"))

        return display_name
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if User._default_manager.filter(email=email).exclude(username=self.cleaned_data.get('user_id')).count():
            raise forms.ValidationError(_("This email has already been registered to another account"))

        validate_email(email)
        return email