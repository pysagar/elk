'''
The urls related to elk app belongs here.
'''

from django.conf.urls import url
from elk_app.forms import ElkPasswordResetForm
from elk_app.views import ELKHome, ELKLogin, UploadFile, KibanaDashboard
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^$', ELKHome.as_view(), name='home'),
    url(r'^login/', ELKLogin.as_view(), name='elk_login'),
    url(r'^logout/', auth_views.logout, {'next_page': '/'}, name='elk_logout'),

    # url for importing file
    url(r'^import/csv/file/', UploadFile.as_view(), name='upload_file'),

    # url for importing file
    url(r'^kibana/dashboard', KibanaDashboard.as_view(), name='kibana_dashboard'),

    # url's for reset/forgot password
    url(r'^password/reset/$',
        auth_views.password_reset,
       {
            'template_name': 'account/password_reset_form.html',
            'email_template_name': 'account/password_reset_email.html',
            'password_reset_form': ElkPasswordResetForm
       }, name='password_reset'),

    url(r'^password/reset/confirm/'r'(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
       auth_views.password_reset_confirm,
       {
           'template_name': 'account/password_reset_confirm.html'
       }, name='password_reset_confirm'),

    url(r'^password/reset/complete/$',
        auth_views.password_reset_complete,
       {
           'template_name': 'account/password_reset_complete.html'
       }, name='password_reset_complete'),

    url(r'^password/reset/done/$',
        auth_views.password_reset_done,
       {
           'template_name': 'account/password_reset_done.html'
       }, name='password_reset_done')
]