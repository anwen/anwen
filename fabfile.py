from fabric.api import run, cd, env, hide
from fabric.api import local

# env.user = 'ask'
# env.hosts = ['local', '58']
# env.key_filename = ["/home/ask/.ssh"]


def hello():
    print("Hello world!")


def host_type():
    run('uname -s')


def test():
    local("make test")


def commit():
    local("git add -p && git commit")


def push():
    local("git push aw_gh")
    local("git push prod")


def prepare_deploy():
    test()
    commit()
    push()


def deploy():
    # todo
    code_dir = '/home/lb/'
    with cd(code_dir):
        host_type()
        run("git pull")


def print_user():
    with hide('running'):
        run('echo "%(user)s"' % env)
