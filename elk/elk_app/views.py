'''
The views related to elk app belongs here.
'''
import os
import datetime
from django.conf import settings
from django.contrib.auth.views import login
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.urlresolvers import reverse_lazy, reverse
from django.http.response import HttpResponseBadRequest, HttpResponse

from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from elk_app.models import LogType, Project, DashboardLink
from elk_app.task import upload_logs


class ELKHome(TemplateView):
    '''
    Renders the home page
    '''
    template_name = '_layout/home.html'

    @method_decorator(login_required(login_url=reverse_lazy('elk_login')))
    def dispatch(self, request, *args, **kwargs):
        return TemplateView.dispatch(self, request, *args, **kwargs)


class ELKLogin(TemplateView):
    '''
    login mechanism based on userID as email and password
    if user is already logged in user will be directed to dashboard
    '''

    template_name = './account/login.html'

    def get(self, request, *args, **kwargs):
        '''
        Overwritten predefined get method.
        '''
        if not request.user.is_authenticated():
            try:
                kwargs['template_name'] = self.get_template_names().pop()
            except AttributeError:
                kwargs['template_name'] = self.get_template_names()
            return login(request, *args, **kwargs)
        else:
            return redirect(reverse('home'))

    def post(self, request, *args, **kwargs):
        '''
        Overwritten predefined post method.
        '''
        if request.POST.get('remember_me', None):
            # Age of cookie, in seconds set to 2 weeks
            request.session.set_expiry(60 * 60 * 24 * 14)

        if not request.user.is_authenticated():
            try:
                kwargs['template_name'] = self.get_template_names().pop()
            except AttributeError:
                kwargs['template_name'] = self.get_template_names()
            return login(request, *args, **kwargs)
        else:
            return redirect(reverse('home'))


class UploadFile(TemplateView):
    '''
    This class uploads the browsed file on server side by
    creating the new file of same type on specified server path.
    '''

    template_name = '_layout/upload.html'

    def get_context_data(self, **kwargs):
        '''
        Overwritten predefined get_context_data method to extract table records from database
        and use these records in template.
        '''
        kwargs['log_types'] = LogType.objects.all()
        kwargs['projects'] = Project.objects.filter(members__in = [self.request.user])
        return kwargs

    def post(self, request, *args, **kwargs):
        '''
        Overwritten predefined post method to call appropriate upload function.
        '''
        file_obj = request.FILES['file']
        project =  request.POST['projects']
        try:
            if file_obj.content_type in ['application/octet-stream', 'text/x-log']:
                filepath = os.path.join(settings.IMPORTFILE_UPLOAD_PATH, file_obj.name)
                newfilepath = default_storage.save(filepath, file_obj)
                log_type = request.POST['log_type']

                timestamp = datetime.datetime.now()
                if log_type == 'Apache' or log_type == 'Nginx':
                    upload_logs.delay(newfilepath, log_type, timestamp, request.user, project, file_obj.name)
                else:
                    raise Exception
            else:
                raise Exception

            return redirect(reverse('upload_file'))

        except Exception:
            return HttpResponseBadRequest('Invalid data supplied.')

    @method_decorator(login_required(login_url=reverse_lazy('elk_login')))
    def dispatch(self, request, *args, **kwargs):
        return TemplateView.dispatch(self, request, *args, **kwargs)


class KibanaDashboard(TemplateView):
    '''
    This class is to show kibana dashboard in iframe.
    '''

    template_name = '_layout/kibana_dashboard.html'

    def get_context_data(self, **kwargs):
        '''
        Overwritten predefined get_context_data method to extract table records from database
        and use these records in template.
        '''
        try:
            kwargs['dashboard_link'] = DashboardLink.objects.get(project__name='NLMS').dashboard_url
        except DashboardLink.DoesNotExist:
            pass
            #TODO implement logger

        return kwargs

    @method_decorator(login_required(login_url=reverse_lazy('elk_login')))
    def dispatch(self, request, *args, **kwargs):
        return TemplateView.dispatch(self, request, *args, **kwargs)