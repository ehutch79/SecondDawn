from django.core.validators import email_re
from django.contrib.auth.models import User

import logging
logger = logging.getLogger( 'django_neve' )

# Overwrite the default backend to check for e-mail address
class EmailBackend:
    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = False

    def authenticate(self, username=None, password=None):
        logger.info('in email auth')

        user = None
        asusername = None
        bits = username.split(' ')
        if len(bits) == 3 and bits[1] == u'as':
            username = bits[0]
            asusername = bits[2]
        
        if email_re.search(username):
            try:
                users = User.objects.filter(email__iexact=username)
                if users.count():
                    user = users[0]

                if user and user.check_password(password):
                    if user.is_superuser and asusername:
                            users = User.objects.filter(email__iexact=asusername)
                            if users.count():
                                user = users[0]

                    return user
            except User.DoesNotExist:
                return None

            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
