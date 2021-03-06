# db.User_Col.validate(true)

import os
from fabric import Connection
from fabric import task
# from fabric import SerialGroup
import time


def free(c):
    uname = c.run('uname -s', hide=True)
    if 'Linux' in uname.stdout:
        command = "df -h / | tail -n1 | awk '{print $5}'"
        return c.run(command, hide=True).stdout.strip()
    # err = "No idea how to get disk space on {}!".format(uname)
    # raise Exit(err)


# c = Connection('aw')


@task
def test(c):
    c = Connection('aw')
    result = c.run('uname -s', hide=True)
    msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"
    print(msg.format(result))
    print(c.run('hostname'))


# @task
# def disk(c):
#     for cxn in SerialGroup('aw', 'aaw'):
#         print("{}: {}".format(cxn, disk_free(cxn)))


# result = c.put('myfiles.tgz', remote='/opt/mydata/')
# print("Uploaded {0.local} to {0.remote}".format(result))


class CD:
    """Context manager for changing the current working directory."""

    def __init__(self, new_path):
        self.new_path = os.path.expanduser(new_path)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.new_path)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


@task
def backol(c):
    c = Connection('aw')
    """ backup data from aw mongo """
    t = time.time()
    with c.cd('/var/www/anwen/db'):
        c.run('. ~/.zshrc && python3 db_in_out.py -o')
        c.run('tar czf aw_yaml_{}.tar.gz data'.format(t))
    with c.cd('/var/www/anwen/docs/shares'):
        c.run('tar czf aw_md_{}.tar.gz *.md'.format(t))
    with c.cd('/var/www/anwen/static/upload/'):
        c.run('tar czf upload_{}.tar.gz img'.format(t))


@task
def backup(c):
    c = Connection('aw')
    """ backup data from aw mongo and download"""
    with c.cd('/var/www/anwen/db'):
        c.run('. ~/.zshrc && python3 db_in_out.py -o')
        c.run('tar czf aw_yaml.tar.gz data')
    with c.cd('/var/www/anwen/docs/shares'):
        c.run('tar czf aw_md.tar.gz *.md')
    with c.cd('/var/www/anwen/static/upload/'):
        c.run('tar czf upload.tar.gz img')
    print('download yaml:')
    with CD(os.path.join(os.getcwd(), 'db/')):
        c.get('/var/www/anwen/db/aw_yaml.tar.gz', 'aw_yaml.tar.gz')
        c.local('tar zxf aw_yaml.tar.gz')
        c.local('rm aw_yaml.tar.gz')
    print('download md:')
    with CD(os.path.join(os.getcwd(), 'docs/shares/')):
        c.get('/var/www/anwen/docs/shares/aw_md.tar.gz', 'aw_md.tar.gz')
        c.local('tar zxf aw_md.tar.gz')
        c.local('rm aw_md.tar.gz')
    print('download img:')
    return
    with CD(os.path.join(os.getcwd(), 'static/upload/')):
        c.get('/var/www/anwen/static/upload/upload.tar.gz', 'upload.tar.gz')
        c.local('tar zxf upload.tar.gz img')
        c.local('rm upload.tar.gz')
