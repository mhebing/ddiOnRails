import os
from pprint import pprint
from fabric import task
from invoke import Collection


from pathlib import Path


# os.environ.setdefault("LC_ALL", "C.UTF-8")
# os.environ.setdefault("LANG", "C.UTF-8")

# os.environ['LC_ALL'] = 'C.UTF-8'
# os.environ['LC_CTYPE'] = 'C.UTF-8'
# os.environ['LANG'] = 'C.UTF-8'

# os.environ['LC_ALL'] = 'en_US.UTF-8'

# pprint(os.environ["LC_ALL"])
# pprint(os.environ["LC_CTYPE"])
# pprint(os.environ["LANG"])


@task
def npm(c):
    """ Install all frontend dependencies with npm """
    c.run("npm install")

@task
def python(c):
    c.run("python --version")
    c.run("python3 --version")
    c.run("which python")
    c.run("which python3")


@task
def venv(c):
    """ Setup the python virtual environment for the project """
    pip = Path.home() / ".envs/ddionrails/bin/pip"
    if not pip.exists():
        print("setting up new virtual environment")
        # c.run("/usr/bin/python3.6 -m venv ~/.envs/ddionrails")
        # c.run("source ~/.envs/ddionrails/bin/activate")
        # c.run("~/.envs/ddionrails/bin/pip3 install -U pip wheel pipenv")
        # c.run("~/.envs/ddionrails/bin/pipenv")

    c.run("source ~/.envs/ddionrails/bin/activate")
    print("updating requirements")
    print("pipenv install --dev")

# os.environ['LC_ALL'] = 'C.UTF-8'
# os.environ['LC_CTYPE'] = 'C.UTF-8'


@task
def pipenv(c):
    """ pipenv """
    c.run("source ~/.envs/ddionrails/bin/activate")
    # c.run("~/.envs/ddionrails/bin/pip -V")
    # c.run("~/.envs/ddionrails/bin/pipenv", replace_env=False)
    # c.run("env", replace_env=False)
    # with c.prefix('LC_ALL=C.UTF-8'):
    #     c.run('echo $LC_ALL')  # prints "production"

    # pipenv = "~/.envs/ddionrails/bin/pipenv"

    # c.run(pipenv, env={"LC_ALL": "C.UTF-8"})

    c.run(
        "~/.envs/ddionrails/bin/pipenv install --dev",
        # env={"LC_ALL": "C.UTF-8", "LANG": "C.UTF-8"},
        replace_env=False, echo=True
    )
    c.run("~/.envs/ddionrails/bin/pipenv graph", replace_env=False)

@task
def piplist(c):
    c.run("~/.envs/ddionrails/bin/pipenv graph", replace_env=False, echo=True)


@task
def django(c):
    c.run("~/.envs/ddionrails/bin/pipenv run django-admin", replace_env=False, echo=True)

@task
def migrate(c):
    # with c.prefix('~/.envs/ddionrails/bin/pipenv shell'):
    c.run("~/.envs/ddionrails/bin/pipenv run ./manage.py migrate", replace_env=False, echo=True)

@task
def server(c):
    # with c.prefix('~/.envs/ddionrails/bin/pipenv shell'):
    c.run("~/.envs/ddionrails/bin/pipenv run ./manage.py runserver", replace_env=False, echo=True)





# inner = Collection('setup', venv, pipenv)
# front = Collection('frontend', npm)
# # inner.configure({'conflicted': 'default value'})
#
# # Our project's root namespace.
# ns = Collection(inner, front)
# # ns.configure({'conflicted': 'override value'})
