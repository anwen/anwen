#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fabric.api import *

env.use_ssh_config = True
# env.hosts = ['aw']
# env.user = 'root'
# env.key_filename = '~/.ssh/aw_rsa'


def hello():
    print("Hello world!")


def whoami():
    run('whoami')


def pwd():
    run('pwd')


def host_type():
    run('uname -s')


@task
def nginx(todo):
    ''' nginx:todo= '''
    # fab -H aw nginx:todo=start
    sudo('/etc/init.d/nginx %s' % todo)


@task
def back_data():
    ''' backup data from aw mongo '''
    with cd('/var/www/anwen/db'):   # 切换到远程目录
        run('./db_in_out.py -o')
        run('tar czf aw_yaml.tar.gz *.yaml')  # 远程解压
    with lcd('~/anwen/db/'):  # 切换到local
        get('/var/www/anwen/db/aw_yaml.tar.gz', '.')
        local('tar zxf aw_yaml.tar.gz')


def test():
    local("make test")


def commit():
    local("git add -p && git add . && git commit -a")


def push():
    local("git push aw_gh")
    local("git push prod")

@task
def deploy():
    test()
    commit()
    push()


def deploy_2():
    # todo
    code_dir = '/home/lb/'
    with cd(code_dir):
        host_type()
        run("git pull")


def print_user():
    with hide('running'):
        run('echo "%(user)s"' % env)
