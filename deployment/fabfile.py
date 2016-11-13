import time
from fabric.api import cd, sudo, task, env


env.sudo_user = 'asi'
env.roledefs = {
    'live': ['bmcalindin-asi.ddns.net'],
}

root = '/data/asi'
releases = root + '/releases'
logs = root + '/logs'
run = root + '/sudo'
git_repo = 'git@github.com:neb42/asi.git'


@task
def initialise_server():
    sudo('mkdir -p {}'.format(releases))
    sudo('mkdir -p {}'.format(logs))
    sudo('mkdir -p {}'.format(run))


@task
def deploy():
    checkout_dir = checkout_revision()
    bootstrap(checkout_dir)
    switch(checkout_dir)
    restart()


@task
def restart():
    # Had some issues with restart on my raspberrypi
    sudo('service apache2 stop', user='root')
    time.sleep(3)
    sudo('service apache2 start', user='root')


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
