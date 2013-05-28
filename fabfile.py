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
env.base = os.path.abspath(os.path.dirname(__file__)) # where this fabfile lives
env.project_root = os.path.join(env.base, env.project_name) # settings dir
env.ve = os.path.dirname(env.base) # one above base

def rm_pyc():
    "Clear all .pyc files that might be lingering"
    local("find . -name '*.pyc' -print0|xargs -0 rm", capture=False)

def drop_database(cmd=local):
    with settings(warn_only=True):
        cmd('dropdb %(db_name)s' % env)

def create_database(cmd=local):
    cmd('createdb -T template_postgis %(db_name)s' % env)
