#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fabric.api import *

env.use_ssh_config = True
# env.hosts = ['aw']
# env.user = 'root'
# env.key_filename = '~/.ssh/aw_rsa'


def test():
    local("make test")


def commit():
    try:
        local("git add -p && git add . && git commit -a")
    except:
        pass


def push():
    local("git push aw_gh")
    local("git push prod")


@hosts(['aw'])
@task
def deploy():
    test()
    commit()
    push()


def deploy_2():
    # todo
    code_dir = '/home/lb/'
    with cd(code_dir):
        run("git pull")


@hosts(['aw'])
@task
def back_data():
    ''' backup data from aw mongo '''
    with cd('/var/www/anwen/db'):   # 切换到远程目录
        run('./db_in_out.py -o')
        run('tar czf aw_yaml.tar.gz data')  # 远程压缩
    with cd('/var/www/anwen/docs/shares'):
        run('tar czf aw_md.tar.gz *.md')  # 远程压缩
    with lcd('~/anwen/db/data/'):  # 切换到local
        get('/var/www/anwen/db/aw_yaml.tar.gz', '.')
        local('tar zxf aw_yaml.tar.gz')
        local('rm zxf aw_yaml.tar.gz')
    with lcd('~/anwen/docs/shares/'):
        get('/var/www/anwen/docs/shares/aw_md.tar.gz', '.')
        local('tar zxf aw_md.tar.gz')
        local('rm zxf aw_md.tar.gz')


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
def update_nginx():
    ''' update_nginx '''

    put('/home/ask/anwen/conf/nginx.conf', '/usr/local/nginx/conf/nginx.conf')
    sudo('/etc/init.d/nginx reload')
