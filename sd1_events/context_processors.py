from django.conf import settings
from django.contrib.sites.models import Site

def stripe(request):
    return { 'STRIPE_SECRET': settings.STRIPE_SECRET, 'STRIPE_PUBLIC': settings.STRIPE_PUBLIC }
    
