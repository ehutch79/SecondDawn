from django import forms
from django.db import models
from django.contrib.auth.forms import SetPasswordForm, AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.validators import validate_email

from sd1_condenser.models import Character, Header, Faction

class CreateCharacterForm(forms.Form):
    name = forms.CharField(max_length=250)

    faction = forms.ChoiceField()
    
    header = forms.ChoiceField()
        
    def clean_name(self):
        name = self.data.get('name')

        if len(name) < 1:
            raise forms.ValidationError(_("Please enter a name!"))


        if Character._default_manager.filter(name=name).count():
            raise forms.ValidationError(_("This name has been taken already"))

        return name
        
    def __init__(self,*args,**kwargs):
        super(CreateCharacterForm,self).__init__(*args,**kwargs)

        self.fields['header'].choices = [(x.pk,x.name) for x in Header.objects.all()]

        self.fields['faction'].choices = [(x.pk,x.name) for x in Faction.objects.filter(beginner=True)]

#        self.fields['some_choices'].choices=[[x,x] for x in list_of_stuff]

        # I used this when I wanted to subclass a built-in form and I 
        # wanted to remove this input
