from fabric.api import *
from fabric.context_managers import *
from fabric.contrib.project import *
from contextlib import contextmanager
import os

env.user = 'chris'
env.roledefs['live'] = ['chris@codeways.org']
project_dir = '/home/chm/Projekte/Web/seotool2'
target_dir = '/srv/apps'


@contextmanager
def virtualenv(dir):
    env.activate = 'source %s/venv/bin/activate' % dir
    with cd(dir):
        with prefix(env.activate):
            yield

@task
def setup():
    dir = os.path.join(target_dir, 'seotool')
    with cd(dir):
        run('virtualenv --distribute --prompt "seotool ~ " venv')
        with virtualenv(dir):
            run('pip install -r ./requirements.txt')


@task
def upload():
    rsync_project(
        remote_dir=os.path.join(target_dir, 'seotool'),
        local_dir=project_dir + os.sep,
        delete=True,
        exclude=['.git', '*.pyc', '.idea', 'venv']
    )


@task
def start():
    dir = os.path.join(target_dir, 'seotool')
    with virtualenv(dir):
        cmd = '%s/venv/bin/python -m seotool.fixtures' % dir
        run(cmd)
        cmd = 'sudo %s/venv/bin/python ./run.py' % dir
        run(cmd)

