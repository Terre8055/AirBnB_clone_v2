#!/usr/bin/python3
# Fabfile to create and distribute an archive to a web server.
import os.path
from datetime import datetime
from fabric import Connection, task


hosts = ["52.86.119.89"]

@task
def do_pack(c):
    """Create a tar gzipped archive of the directory web_static."""
    dt = datetime.utcnow()
    file = "versions/web_static_{}{}{}{}{}{}.tgz".format(dt.year,
                                                         dt.month,
                                                         dt.day,
                                                         dt.hour,
                                                         dt.minute,
                                                         dt.second)
    if os.path.isdir("versions") is False:
        if c.run("mkdir -p versions").ok is False:
            return None
    if c.run("tar -cvzf {} web_static".format(file)).ok is False:
        return None
    return file

@task
def do_deploy(c, archive_path):
    """Distributes an archive to a web server.
    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if os.path.isfile(archive_path) is False:
        return False
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]
    for host in hosts:
        c = Connection(host = host, user = 'ubuntu')
        c.put(archive_path, "/tmp/{}".format(file))
        if c.run("sudo rm -rf /data/web_static/releases/{}/".
               format(name)).ok is False:
            return False
        if c.run("sudo mkdir -p /data/web_static/releases/{}/".
               format(name)).ok is False:
            return False
        if c.run("sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
               format(file, name)).ok is False:
            return False
        if c.run("sudo rm /tmp/{}".format(file)).ok is False:
            return False
        if c.run("sudo mv /data/web_static/releases/{}/web_static/* "
               "/data/web_static/releases/{}/".format(name, name)).ok is False:
            return False
        if c.run("sudo rm -rf /data/web_static/releases/{}/web_static".
               format(name)).ok is False:
            return False
        if c.run("sudo rm -rf /data/web_static/current").ok is False:
            return False
        if c.run("sudo ln -s /data/web_static/releases/{}/ /data/web_static/current".
               format(name)).ok is False:
            return False
    return True

@task
def deploy(c):
    """Create and distribute an archive to a web server."""
    file = do_pack(c)
    if file is None:
        return False
    return do_deploy(c, file)
