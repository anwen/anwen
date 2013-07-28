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
    import os
    ''' backup data from aw mongo '''
    with cd('/var/www/anwen/db'):   # 切换到远程目录
        run('chmod +x db_in_out.py')
        run('./db_in_out.py -o')
        run('tar czf aw_yaml.tar.gz data')  # 远程压缩
    with cd('/var/www/anwen/docs/shares'):
        run('tar czf aw_md.tar.gz *.md')  # 远程压缩
    with cd('/var/www/anwen/static/upload/'):
        run('tar czf upload.tar.gz *')  # 远程压缩
    with lcd(os.path.join(os.getcwd(), 'db/')):  # 切换到local
        get('/var/www/anwen/db/aw_yaml.tar.gz', '.')
        local('tar zxf aw_yaml.tar.gz')
        local('rm aw_yaml.tar.gz')
    with lcd(os.path.join(os.getcwd(), 'docs/shares/')):
        get('/var/www/anwen/docs/shares/aw_md.tar.gz', '.')
        local('tar zxf aw_md.tar.gz')
        local('rm aw_md.tar.gz')
    with lcd(os.path.join(os.getcwd(), 'static/upload/')):
        get('/var/www/anwen/static/upload/upload.tar.gz', '.')
        local('tar zxf upload.tar.gz')
        local('rm upload.tar.gz')


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
