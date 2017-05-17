'''
Customised forms should be written here.
'''

from django.contrib.auth.forms import PasswordResetForm
from django import forms
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail.message import EmailMultiAlternatives
from django.template import loader
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from elk_app.models import User


class ElkPasswordResetForm(PasswordResetForm):
    '''
    Customised password reset form.
    '''
    def __init__(self, *args, **kwargs):
        super(ElkPasswordResetForm, self).__init__(*args, **kwargs)
        self.fields['email'].error_messages['required'] = 'Please enter an email address'

    def clean_email(self):
        '''
         only registered user can get password reset link
        '''
        email = self.data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('Given email is not registered')
        else:
            return email

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        '''
        Generates a one-use only link for resetting password and sends to the
        user.
        '''

        UserModel = get_user_model()
        email = self.cleaned_data['email']
        active_users = UserModel.objects.filter(email__iexact=email, is_active=True)
        for user in active_users:
            # Make sure that no email is sent to a user that actually has
            # a password marked as unusable
            if not user.has_usable_password():
                continue
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            context = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
            }
            subject = loader.render_to_string(subject_template_name, context)
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            message = loader.render_to_string(email_template_name, context)
            if extra_email_context is not None:
                context.update(extra_email_context)
            self.send_mail(subject, message, from_email, [user.email])

    def send_mail(self, subject, message, from_email, recipients):
        '''
        Send mail to reset password.
        '''
        mail = EmailMultiAlternatives('%s' % (subject),
                                      message, from_email, recipients)
        mail.attach_alternative(message, 'text/html')
        mail.send(fail_silently=True)


