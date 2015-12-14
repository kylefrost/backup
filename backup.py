# -*- coding: utf-8 -*-

#
#  backup.py
#  By: Kyle Frost
#  Date: December 12, 2015
#  Purpose: Back up important
#           files on web server
#           and scp to network drive.
#


import time
import scp
import paramiko
import zipfile
import shutil
import os
import tweet
import time

BTIME = str(int(time.time()))
BACKUP_FILENAME = "backup" + BTIME
# Not traditional /tmp for size reasons, instead backup to /mnt/stor (128GB drive)
BACKUP_DIR = "/mnt/stor/tmp/" + BACKUP_FILENAME + "/"
SCP_DIR = "/Volumes/External HD/RPi/BACKUPS/"

class Backup:
    # Handles Backup related functions

    def __init__(self, backup_dir=None, backup_filename=None, scp_dir=None):
        # Backup init handler

        self.backup_dir = BACKUP_DIR
        self.backup_filename = BACKUP_FILENAME
        self.scp_dir = SCP_DIR

    def copy(self, path):
        # Copy `path` to backup directory

        if os.path.isdir(path):
            # path is a directory
            pass
        else:
            # path is a file
            pass

    def archive(self):
        # Archive backup directory
        
        pass

    def send(self, addr, remote_path):
        # Send file to addr:remote_path
        
        ssh = paramiko.SSHClient()
        ssh.load_system_keys()
        ssh.connect("10.0.1.2")

        with scp.SCPClient(ssh.get_transport()) as scpc:
            scpc.put(BACKUP_FILENAME + ".zip", SCP_DIR + BACKUP_FILENAME + ".zip")

        ssh.close()

    def error(self, errormsg):
        print "! " + errormsg

    def success(self, successmsg):
        print u"✓ " + successmsg

def main():
    # Main function

    backup = Backup()

    try:
        # Things to backup
        # /home
        # /etc/apache2
        # /var/www
        # /etc/crontab
        # pip packages
        # apt packages
        # MySQL databases
        backup.success("Backup was successful.")
    except:
        backup.error("Backup was unsuccessul.")
 
if __name__ == "__main__":
    main()
