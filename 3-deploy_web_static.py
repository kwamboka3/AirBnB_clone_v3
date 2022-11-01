#!/usr/bin/python3
'''Deploy module'''
from os import path
import datetime
from fabric.api import local, run, put, env


env.hosts = ['3.236.44.4', '3.235.147.115']


def deploy():
    '''Creates and distributes an archive
    to your web servers'''
    filename = do_pack()
    if filename is None:
        return False
    answer = do_deploy(filename)
    return answer


def do_pack():
    '''Create a tarball file of web static'''
    fecha = datetime.datetime.now().isoformat()
    fecha = fecha[:-7].replace(":", "").replace(
        ".", "").replace("T", "").replace("-", "")
    filename = "versions/web_static_" + fecha + ".tgz"
    if not path.exists('versions'):
        try:
            local("mkdir -p versions")
        except:
            return None
    try:
        local("tar -czvf {} web_static".format(filename))
    except:
        return None
    return filename


def do_deploy(archive_path):
    '''Distributes an archive to your web servers,
    using the function do_deploy'''
    filename = archive_path[9:-4]

    if not path.exists(archive_path):
        return False
    if put(archive_path, "/tmp/").failed:
        return False
    '''if run("sudo rm -rf /data/web_static/releases/{}/"
           .format(filename)).failed:
        return False'''
    if run("sudo mkdir -p /data/web_static/releases/{}/"
           .format(filename)).failed:
        return False
    if run('sudo tar -zxf /tmp/{} -C /data/web_static/releases/{}/'
           .format(filename + ".tgz", filename)).failed:
        return False
    if run('sudo rm /tmp/{}'.format(filename + '.tgz')).failed:
        return False
    if run('sudo mv /data/web_static/releases/{}/web_static/*'
           ' /data/web_static/releases/{}/'
           .format(filename, filename)).failed:
        return False
    if run('sudo rm -rf /data/web_static/releases/{}/web_static'
           .format(filename)).failed:
        return False
    if run('sudo rm -rf /data/web_static/current').failed:
        return False
    if run('sudo ln -s /data/web_static/releases/{}/ /data/web_static/current'
           .format(filename)).failed:
        return False

    return True
