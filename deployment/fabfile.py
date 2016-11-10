import time
from fabric.api import cd, sudo, task, env


env.roledefs = {
    'dev': ['82.2.82.169'],
    'live': [],
}



root = '/data/asi'
releases = root + '/releases'
logs = root + '/logs'
run = root + '/sudo'
git_repo = 'git@github.com:neb42/asi.git'
env.sudo_user = 'asi'


@task
def initialise_server():
    #sudo('install git')
    #sudo('install apache')
    #sudo('install mod wsgi')
    sudo('mkdir -p {}'.format(releases))
    sudo('mkdir -p {}'.format(logs))
    sudo('mkdir -p {}'.format(run))


@task
def deploy():
    checkout_dir = checkout_revision()
    bootstrap(checkout_dir)
    switch(checkout_dir)
    restart()


def checkout_revision(revision='latest'):
    t = int(time.time())
    with cd(releases):
        if revision == 'latest':
            sudo('git clone {} latest'.format(git_repo))
            with cd('latest'):
                revision = sudo('git log | head -n1').split(' ')[1]
            sudo('mv latest {}_{}'.format(revision, t))
        else:
            sudo('git clone {} {}_{}'.format(git_repo, revision, t))
            with cd('{}_{}'.format(revision, t)):
                sudo('git checkout {}'.format(revision))
    return '{}_{}'.format(revision, t)


def bootstrap(checkout_dir):
    with cd('{}/{}'.format(releases, checkout_dir)):
        sudo('./bootstrap')


def switch(checkout_dir):
    with cd(releases):
        sudo('ln -sfn {}/{} current'.format(releases, checkout_dir))


def restart():
    sudo('/etc/init.d/apache2 restart')


def get_current_role():
    roles = filter(lambda x: env.host_string in x[1], env.roledefs.items())
    if len(roles) != 1:
        raise Exception('Invalid number of roles')
    return roles[0][0]
