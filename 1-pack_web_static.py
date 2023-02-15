#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from the contents of
the 'web_static' folder"""
from datetime import datetime

from fabric.api import env, local, run, sudo, put

env.user = 'ubuntu'
web1 = '54.90.15.29'
web2 = '18.207.207.53'
env.hosts = [web1, web2]


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


def set_up():
    '''Sets up the web servers for the deployment of web_static using
    "0-setup_web_static.sh" bash script'''

    put('0-setup_web_static.sh', mirror_local_mode=True)
    # code = sudo('./0-setup_web_static.sh').return_code
    code = run('./0-setup_web_static.sh').return_code
    run('rm -f 0-setup_web_static.sh')

    print('Set up script was run and exited with exit code {}\n'.format(code))
