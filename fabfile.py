#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from fabric.api import task, env, local, hosts, cd, run, lcd, get, sudo, put

env.use_ssh_config = True


def test():
    local("make test")


@task
def commit():
    try:
        local("git add -p && git add . && git commit -a")
    except:
        pass

def push():
    local("git push aw_gh")
    local("git push prod")


@task
def deploy():
    test()
    commit()
    push()


@hosts(['aw'])
@task
def back_data():
    ''' backup data from aw mongo '''
    with cd('/var/www/anwen/db'):
        run('chmod +x db_in_out.py')
        run('./db_in_out.py -o')
        run('tar czf aw_yaml.tar.gz data')
    with cd('/var/www/anwen/docs/shares'):
        run('tar czf aw_md.tar.gz *.md')
    with cd('/var/www/anwen/static/upload/'):
        run('tar czf upload.tar.gz img')
    with lcd(os.path.join(os.getcwd(), 'db/')):
        get('/var/www/anwen/db/aw_yaml.tar.gz', '.')
        local('tar zxf aw_yaml.tar.gz')
        local('rm aw_yaml.tar.gz')
    with lcd(os.path.join(os.getcwd(), 'docs/shares/')):
        get('/var/www/anwen/docs/shares/aw_md.tar.gz', '.')
        local('tar zxf aw_md.tar.gz')
        local('rm aw_md.tar.gz')
    with lcd(os.path.join(os.getcwd(), 'static/upload/')):
        get('/var/www/anwen/static/upload/upload.tar.gz', '.')
        local('tar zxf upload.tar.gz img')
        local('rm upload.tar.gz')


@task
def nginx(todo):
    ''' nginx:todo= '''
    # fab -H aw nginx:todo=start
    sudo('/etc/init.d/nginx %s' % todo)


@hosts(['aw'])
@task
def update_nginx():
    ''' update_nginx '''
    nginx_file = os.path.join(os.getcwd(), 'conf/nginx.conf')
    put(nginx_file, '/usr/local/nginx/conf/nginx.conf')
    sudo('/etc/init.d/nginx reload')
