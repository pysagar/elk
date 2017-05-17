import os
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from django.core.files.storage import default_storage
from elk.settings import LOGSTASH_ROOT
from elk_app.models import UploadDetail, Project, LogType


class LogUpload():
    '''
    To bulk upload apache logs from log file.
    '''
    def __init__(self, file_path, log_type, time, current_user, project, file_name):
        self.filepath = file_path
        self.project = project
        self.file_name = file_name
        self.log_type = log_type
        self.logstash_root = LOGSTASH_ROOT
        self.time = time
        self.current_user = current_user
        self.unprocessed_rows = []

    def cleanup(self):
        '''
        Removes uploaded file
        '''
        default_storage.delete(self.filepath)

    def run(self):
        '''
        This function used to automatically upload apache logs.
        '''
        try:
            project = Project.objects.get(name=self.project)
            project_name = project.name.lower()
            log_type = LogType.objects.get(name=self.log_type)

            upload_details = UploadDetail.objects.get(
                user=self.current_user, project=project, file_name=self.file_name, log_type=log_type)

        except UploadDetail.DoesNotExist:
            upload_details = UploadDetail.objects.create(
                user=self.current_user, project=project, file_name=self.file_name, log_type=log_type)

            os.system('cat {} | {}/logstash -f {}/{}.conf'.format(self.filepath, self.logstash_root, self.logstash_root, project_name))
            self.cleanup()

        except Project.DoesNotExist:
            pass
            #TODO implement logger

        except LogType.DoesNotExist:
            pass
            #TODO implement logger

        except AttributeError:
            pass
            #TODO implement logger

        except MultipleObjectsReturned:
            UploadDetail.objects.last().delete()
