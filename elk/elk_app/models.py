from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser, Group

from django.db import models

import string
import random

# Create your models here.


class Role(models.Model):
    '''
    User role model.
    '''
    name = models.CharField(max_length=20)
    group = models.ForeignKey(Group, help_text='FA groups', related_name='role_group')
    # meta field
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name


class User(AbstractUser):
    '''
    User profile table with common user fields.
    '''
    role = models.ForeignKey(Role, null=True, help_text='User Roles', related_name='user_role')
    dob = models.DateField(blank=True, null=True)
    # meta field
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return ('%s %s' % (self.first_name, self.last_name)) or self.user.username

    def set_random_username(self, length=30, chars='', split=0, delimiter='-'):
        '''
        method to set random username.
        '''
        chars = chars or (string.ascii_letters + string.digits)
        username = ''.join(random.sample(chars, 30))
        if split:
            username = delimiter.join(
                [username[start:start + split] for start in range(0, len(username), split)])
        try:
            User.objects.get(username=username)
            self.generate_random_username(length=length, chars=chars, split=split,
                                          delimiter=delimiter)
        except User.DoesNotExist:
            self.username = username

    def save_password(self):
        try:
            self.set_password(self.password)
        except TypeError:
            pass
            #TODO implement logger.

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        '''
        Overwritten predefined save method to assign permission after save.
        '''
        if not self.username:
            self.set_random_username(length=10)

        response = AbstractUser.save(self, force_insert=force_insert, force_update=force_update,
                                     using=using, update_fields=update_fields)

        if not self.has_usable_password():
            self.save_password()
            self.save()

        return response

class Project(models.Model):
    '''
    Project model that describes it's owner and its project members.
    '''
    name = models.CharField(max_length=200)
    # owner = models.ForeignKey(User, help_text='Project owner', related_name='project_owner')
    members = models.ManyToManyField(User, help_text='Project members', related_name='project_members')
    # meta field
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name


class LogType(models.Model):
    '''
    Logs model describes type of log.
    '''
    name = models.CharField(max_length=200)
    # meta field
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name


class ProjectLog(models.Model):
    '''
    ProjectLogs describes relation between project and logs
    '''
    project = models.ForeignKey(Project, help_text='FA projects')
    log_type = models.ForeignKey(LogType, help_text='Log type')
    # meta field
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "{}-{}".format(self.project.name, self.logs_type.name)


class UploadDetail(models.Model):
    '''
    UploadDetails describe the details of file that are uploaded till the date along with the uploader.
    '''
    user = models.ForeignKey(User, help_text='FA users')
    project = models.ForeignKey(Project, help_text='FA projects')
    file_name = models.CharField(max_length=50)
    log_type = models.ForeignKey(LogType, help_text='Log type')
    # meta field
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "{}-{}-{}-{}".format(self.user, self.project.name, self.file_name, self.log_type.name)


class DashboardLink(models.Model):
    '''
    DashboardLink describes the url link to dashboard for specific user over specific project.
    '''
    project = models.ForeignKey(Project, help_text='FA projects')
    dashboard_url = models.URLField()
    # meta field
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "{}-{}".format(self.project.name, self.dashboard_url)

