from django.core.mail import BadHeaderError, send_mail
from django.template.loader import get_template
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

def send_welcome_email(user, request):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    to = user.email

    subject_template = get_template('registration/welcome_subject.txt')
    subject_context = {'username': user.username}
    subject_content = subject_template.render(subject_context)

    body_template = get_template('registration/welcome_email.txt')
    body_context = {
        'protocol': 'https' if request.is_secure() else 'http',
        'domain': request.META['HTTP_HOST'],
        'username': user.username,
        'uid': uid,
        'token': token
    }
    body_content = body_template.render(body_context)

    try:
        send_mail(subject_content, body_content, None, [to])
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
