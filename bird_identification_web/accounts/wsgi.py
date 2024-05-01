# This file contains a mod_wsgi handler that checks if user is logged in

from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session

def check_password(environ, username, session_key): # Password is session_key
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        return None
    
    try:
        session = Session.objects.get(session_key=session_key)
    except ObjectDoesNotExist:
        return False
    else:
        if session.get_decoded().get('_auth_user_id') == str(user.id):
            return True
        else:
            return False
