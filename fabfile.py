import datetime
import os
import sys
from fabric.api import *
from fabric.contrib import django

# names
env.db_name = "colorado"
env.ve_name = "colorado"
env.repo_name = "colorado"
env.project_name = "colorado"

# paths
env.base = os.path.realpath(os.path.dirname(__file__)) # where this fabfile lives
env.project_root = os.path.join(env.base, env.project_name) # settings dir
env.ve = os.path.dirname(env.base) # one above base

# executables
env.python = os.path.join(env.ve, 'bin', 'python')
env.manage = "%(python)s %(base)s/manage.py" % env

# environment
env.exclude_requirements = [
    'wsgiref', 'readline', 'ipython',
    'git-remote-helpers',
]

def rm_pyc():
    "Clear all .pyc files that might be lingering"
    local("find . -name '*.pyc' -print0|xargs -0 rm", capture=False)

def drop_database():
    "Drop database. Don't do this by accident."
    with settings(warn_only=True):
        local('dropdb %(db_name)s' % env)

def create_database():
    "Create our local database."
    local('createdb -T template_postgis %(db_name)s' % env)

def reset():
    "Drop and recreate the local database."
    rm_pyc()
    drop_database()
    create_database()

    manage('syncdb --noinput')
    manage('migrate')

def manage(cmd):
    """
    Run a Django management command in this VE.
    Really only useful in other fab commands.
    """
    local('%s %s' % (env.manage, cmd))

def freeze():
    """
    pip freeze > requirements.txt, excluding virtualenv clutter
    """
    reqs = local('pip freeze', capture=True).split('\n')
    reqs = [r for r in reqs if r.split('==')[0] not in env.exclude_requirements]
    reqs = '\n'.join(reqs)

    with open('requirements.txt', 'wb') as f:
        f.write(reqs)

    print reqs



