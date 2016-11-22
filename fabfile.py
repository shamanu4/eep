"""
Starter fabfile for deploying the ecity project.

Change all the things marked CHANGEME. Other things can be left at their
defaults if you are happy with the default layout.
"""

import posixpath

from fabric.api import run, local, env, settings, cd, task, sudo
from fabric.contrib.files import exists
from fabric.operations import _prefix_commands, _prefix_env_vars
from copy import deepcopy

#from fabric.decorators import runs_once
#from fabric.context_managers import cd, lcd, settings, hide


# CHANGEME
env.hosts = ['maxim@192.168.33.152']
env.project_main_app = 'EEP'
env.project_name = None
env.commit = None

ENVIRONMENTS = {
    'production': {
        'env.project_name': 'eep'
    },

    'staging': {
        'env.project_name': 'eep-staging'
    },

    'rolling': {
        'env.project_name': 'eep-rolling'
    },
}


def update_env():
    env.code_dir = '/home/maxim/production/%s' % env.project_name
    env.project_dir = '/home/maxim/production/%s/%s' % (env.project_name, env.project_main_app)
    env.static_root = '/home/maxim/production/%s/static/' % env.project_name
    env.virtualenv = '/home/maxim/production/%s/env' % env.project_name
    env.code_repo = 'git@bitbucket.org:timdevs/eep.git'
    env.django_settings_module = '%s.settings' % env.project_main_app


# Python version
PYTHON_BIN = "python3.5"
PYTHON_PREFIX = ""  # e.g. /usr/local  Use "" for automatic
PYTHON_FULL_PATH = "%s/bin/%s" % (PYTHON_PREFIX, PYTHON_BIN) if PYTHON_PREFIX else PYTHON_BIN

# Set to true if you can restart your webserver (via wsgi.py), false to stop/start your webserver
# CHANGEME
DJANGO_SERVER_RESTART = False


def virtualenv(venv_dir):
    """
    Context manager that establishes a virtualenv to use.
    """
    return settings(venv=venv_dir)


def run_venv(command, **kwargs):
    """
    Runs a command in a virtualenv (which has been specified using
    the virtualenv context manager
    """
    run("source %s/bin/activate" % env.virtualenv + " && " + command, **kwargs)


def install_dependencies():
    ensure_virtualenv()
    with virtualenv(env.virtualenv):
        with cd(env.code_dir):
            run_venv("pip install -U pip")
            run_venv("pip install -Ur requirements.txt")


def ensure_virtualenv():
    if exists(env.virtualenv):
        return

    with cd(env.code_dir):
       run("%s -m venv %s" %
           (PYTHON_BIN, env.virtualenv))
       run("echo %s > %s/lib/%s/site-packages/projectsource.pth" %
           (env.project_dir, env.virtualenv, PYTHON_BIN))


def ensure_static_root():
    if exists(env.static_root):
        return

    with cd(env.code_dir):
       run("mkdir -p %s" % env.static_root)


def ensure_src_dir():
    if not exists(env.code_dir):
       run("mkdir -p %s" % env.code_dir)
    with cd(env.code_dir):
       if not exists(posixpath.join(env.code_dir, '.git')):
           run('git clone %s .' % (env.code_repo))


def push_sources():
    """
    Push source code to server
    """
    ensure_src_dir()
    local('git push origin master')
    with cd(env.code_dir):
        run('git fetch')
        if env.commit:
            run('git reset --hard %s' % env.commit)
        else:
            run('git reset --hard origin/master')


@task
def run_tests():
    """ Runs the Django test suite as is.  """
    local("./manage.py test")


@task
def compile_translation():
    """ Runs the Django test suite as is.  """
    with virtualenv(env.virtualenv):
        with cd(env.code_dir):
            run_venv("./manage.py compilemessages -l uk")


@task
def version():
    """ Show last commit to the deployed repo. """
    with cd(env.code_dir):
        run('git log -1')


@task
def uname():
    """ Prints information about the host. """
    run("uname -a")


@task
def webserver_stop():
    """
    Stop the webserver that is running the Django instance
    """
    with virtualenv(env.virtualenv):
        sudo("supervisorctl stop %s" % env.project_name)

@task
def webserver_restart():
    """
    Restarts the webserver that is running the Django instance
    """
    #if DJANGO_SERVER_RESTART:
    #    with cd(env.code_dir):
    #        run("touch %s/wsgi.py" % env.project_dir)
    #else:
    #    #with settings(warn_only=True):
    #    #    webserver_stop()
    #    webserver_restart()
    with virtualenv(env.virtualenv):
        sudo("supervisorctl restart %s" % env.project_name)


#def restart():
#    """ Restart the wsgi process """
#    with cd(env.code_dir):
#        run("touch %s/ecity/wsgi.py" % env.code_dir)


def build_static():
    ensure_static_root()
    assert env.static_root.strip() != '' and env.static_root.strip() != '/'
    with virtualenv(env.virtualenv):
        with cd(env.code_dir):
            run_venv("./manage.py collectstatic -v 0 --clear --noinput")

    run("chmod -R ugo+r %s" % env.static_root)


@task
def first_deployment_mode():
    """
    Use before first deployment to switch on fake south migrations.
    """
    env.initial_deploy = True


@task
def update_database(app=None):
    """
    Update the database (run the migrations)
    Usage: fab update_database:app_name
    """
    with virtualenv(env.virtualenv):
        with cd(env.code_dir):
            if getattr(env, 'initial_deploy', False):
                run_venv("./manage.py migrate --fake --noinput")
            else:
                if app:
                    run_venv("./manage.py migrate %s --noinput" % app)
                else:
                    run_venv("./manage.py migrate --noinput")


@task
def sshagent_run(cmd):
    """
    Helper function.
    Runs a command with SSH agent forwarding enabled.

    Note:: Fabric (and paramiko) can't forward your SSH agent.
    This helper uses your system's ssh to do so.
    """
    # Handle context manager modifications
    wrapped_cmd = _prefix_commands(_prefix_env_vars(cmd), 'remote')
    try:
        host, port = env.host_string.split(':')
        return local(
            "ssh -p %s -A %s@%s '%s'" % (port, env.user, host, wrapped_cmd)
        )
    except ValueError:
        return local(
            "ssh -A %s@%s '%s'" % (env.user, env.host_string, wrapped_cmd)
        )


@task
def switch(e):
    if e in ENVIRONMENTS:
        ename = ENVIRONMENTS[e]
        for key in ename:
            module, attr = key.split(".")
            if module in globals():
                setattr(globals()[module], attr, ename[key])
            else:
                raise RuntimeWarning("environment variable %s is not defined" % module)
        update_env()
    else:
        print("choose valid env: (%s) " % ",".join(ENVIRONMENTS.keys()))


@task
def commit(c):
    env.commit = c


@task
def deploy():
    """
    Deploy the project.
    """
    # with settings(warn_only=True):
    #     webserver_stop()

    if not env.project_name:
        print("choose valid env: (%s). Command switch:e=<ENVIRONMENT>" % ",".join(ENVIRONMENTS.keys()))
    else:
        push_sources()
        install_dependencies()
        update_database()
        build_static()
        compile_translation()
        webserver_restart()
