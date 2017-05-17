from celery import task

@task()
def upload_logs(filepath, log_type, timestamp, user, project, file_name):
    '''
    Task for file upload of learners
    '''
    from elk_app.upload import LogUpload

    processor = LogUpload(filepath, log_type, timestamp, user, project, file_name)
    processor.run()
