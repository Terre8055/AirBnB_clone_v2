#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""

from datetime import datetime
from fabric import task, Connection
import os

hosts = ["52.86.119.89", "54.172.232.200"]
user = "ubuntu"

@task
def do_pack(c):
    """
        return the archive path if archive has generated correctly.
    """

    c.run("mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    archived_f_path = "versions/web_static_{}.tgz".format(date)
    t_gzip_archive = c.run("tar -cvzf {} web_static".format(archived_f_path))

    if t_gzip_archive.ok:
        print("Archive created: {}".format(archived_f_path))
        return archived_f_path
    else:
        return None

@task
def do_deploy(c, archive_path):
    """
        Distribute archive.
    """
    if os.path.exists(archive_path):
        archived_file = archive_path[9:]
        newest_version = "/data/web_static/releases/" + archived_file[:-4]
        archived_file = "/tmp/" + archived_file
        for host in hosts:
            c = Connection(host = host, user = 'ubuntu')
            c.put(archive_path, "/tmp/")
            c.run("sudo mkdir -p {}".format(newest_version))
            c.run("sudo tar -xzf {} -C {}/".format(archived_file,
                                                 newest_version))
            c.run("sudo rm {}".format(archived_file))
            c.run("sudo mv {}/web_static/* {}".format(newest_version,
                                                    newest_version))
            c.run("sudo rm -rf {}/web_static".format(newest_version))
            c.run("sudo rm -rf /data/web_static/current")
            c.run("sudo ln -s {} /data/web_static/current".format(newest_version))

        print("New version deployed!")
        return True

    return False
