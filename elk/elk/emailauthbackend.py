'''
Email authentication backend.
'''

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()


class EmailAuthBackend(ModelBackend):
    """
    Email Authentication Backend
    Allows a user to sign in using an email/password pair rather than
    a username/password pair.
    """

    def authenticate(self, username=None, password=None):
        '''
        Authenticate a user based on email address as the user name.
        '''
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        '''
        Get a User object from the user_id.
        '''
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
