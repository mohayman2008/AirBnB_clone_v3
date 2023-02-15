#!/usr/bin/python3
"""Fabric script to deploy HBNB web_staic on the remote servers"""
from datetime import datetime
import os

from fabric.api import env, local, run, sudo, put, runs_once

env.user = 'ubuntu'
web1 = '54.90.15.29'
web2 = '18.207.207.53'
env.hosts = [web1, web2]


@runs_once
def do_pack():
    '''Packs the contents of the 'web_static' folder to a .tgz archive'''

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    directory = 'versions'
    filename = 'web_static_' + timestamp + '.tgz'
    path = '{}/{}'.format(directory, filename)

    local('mkdir -p {}'.format(directory))

    if (local('tar -cvzf {} web_static'.format(path)).failed):
        return None
    return path


def do_deploy(archive_path):
    '''Distributes an archive to the remote web servers'''

    if not archive_path or not os.path.exists(archive_path):
        return False

    fn = os.path.basename(archive_path)
    tmp_path = '/tmp/' + fn
    remote_path = '/data/web_static/releases/' + fn[:-4] + '/'

    if (put(archive_path, tmp_path, mirror_local_mode=True).failed):
        return False
    if (run('mkdir -p {}'.format(remote_path)).failed):
        return False
    if (run('tar -xzf {} -C {}'.format(tmp_path, remote_path)).failed):
        return False
    if (run('rm -f {}'.format(tmp_path)).failed):
        return False
    if (run('mv -f {0}web_static/* {0}'.format(remote_path)).failed):
        return False

    if (run('rm -rf {}web_static/'.format(remote_path)).failed):
        return False
    if (run('rm -f /data/web_static/current').failed):
        return False
    command = 'ln -sf {} {}'.format(remote_path, '/data/web_static/current')
    if (run(command).failed):
        return False

    print('Deployed successfully.\n')
    return True


def deploy():
    '''Creates and Distributes an archive to the remote web servers'''

    path = do_pack()
    if path is None:
        return False
    return (do_deploy(path))


def set_up():
    '''Sets up the web servers for the deployment of web_static using
    "0-setup_web_static.sh" bash script'''

    put('0-setup_web_static.sh', mirror_local_mode=True)
    # code = sudo('./0-setup_web_static.sh').return_code
    code = run('./0-setup_web_static.sh').return_code
    run('rm -f 0-setup_web_static.sh')

    print('Set up script was run and exited with exit code {}\n'.format(code))
