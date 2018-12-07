import os
import shutil
from pprint import pprint

from django.contrib.auth import get_user_model

from fabric.colors import cyan, green
from fabric.context_managers import cd, hide
from fabric.contrib import django
from fabric.decorators import roles, task
from fabric.operations import env, local, prompt, run, sudo
from fabric.tasks import execute
from fabric.utils import puts

env.project_name = 'ddionrails'


BASE_DIR = os.path.dirname(os.path.realpath(__file__))
print(BASE_DIR)
django.settings_module('settings.development')


import django # isort:skip
django.setup()


ADMIN_EMAIL_ADDRESS = 'admin@example.com'

# env.project_name = '{{ project_name }}'
env.project_root_dir = os.path.dirname(os.path.abspath(__file__))

env.project_src_dir = env.project_root_dir

env.hosts = ['localhost']


def pipenv_run(command):
    """
    Run a "pipenv run" command on the server.
    """
    with cd(env.project_src_dir):
        run('pipenv run {pipenv_command}'.format(pipenv_command=command, **env))


def pipenv_run_local(command):
    """
    Run a "pipenv run" command locally.
    """
    local('pipenv run {pipenv_command}'.format(pipenv_command=command, **env))


@task
def migrate():
    """
    Run DB migrations.
    """
    pipenv_run_local('python manage.py migrate')

@task
def python(c):
    c.run("python --version")
    c.run("python3 --version")
    c.run("which python")
    c.run("which python3")



@task
def pipenv():
    pprint(env)



    run("which python")
    # local("pipenv")


@task
def pipenv_requirements():
    """
    Update the requirements using global pipenv.
    """
    with cd(env.project_src_dir):
        run('pipenv install --dev')


@task
def copy_secrets_file():
    """ Copy the secrets.json.example and rename it to secrets.json """
    shutil.copyfile("secrets.json.example", "secrets.json")
