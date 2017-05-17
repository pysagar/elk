'''
fabfile to setup te project.
'''

import os
import sys

from fabric.api import (env, task, run, cd)

CURRENT_DIR = os.path.abspath(os.path.dirname(__name__))

DJ_APP = lambda: env.code_root
LOGSTASH_DIR = lambda: env.logstash_root


def setup_env():
    '''
    decorator to set env variables based on the host
    '''
    if env.venv_root:
        env.venv_path = os.path.join(env.venv_root, env.venv_name)
    else:
        env.venv_path = os.path.join(env.project_root, env.venv_name)

    env.code_root = os.path.join(env.project_root, env.project_name)

    path = os.path.abspath(os.path.join(os.path.dirname(__file__), env.project_name))
    sys.path.insert(0, path)


def _load_apache_logs(log_type):
    log_parse_file = log_type + '.conf'
    with cd(LOGSTASH_DIR()):
        run('cat /home/sagar/Downloads/nginx_access_logs/timesheet/access.log.30 | ./logstash -f ./{}'.format(log_parse_file))

def _load_nginx_logs():
    pass

def load_logs_to_elasticsearch(log_type):
    _load_apache_logs(log_type)

@task
def elk(log_type):
    '''
    This command is to parse and load apache/nginx logs to elastic search.
    '''
    setup_env()
    load_logs_to_elasticsearch(log_type)