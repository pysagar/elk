from django.contrib import admin

# Register your models here.
from elk_app.models import Role, User, Project, LogType, ProjectLog, UploadDetail, DashboardLink

admin.site.register(Role)
admin.site.register(User)
admin.site.register(Project)
admin.site.register(LogType)
admin.site.register(ProjectLog)
admin.site.register(UploadDetail)
admin.site.register(DashboardLink)