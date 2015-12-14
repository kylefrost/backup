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
import shutil
import os
import tweet
import time
import datetime

BTIME = str(int(time.time()))
BACKUP_FILENAME = "backup" + BTIME
# Not traditional /tmp for size reasons, instead backup to /mnt/stor (128GB drive)
BACKUP_DIR = "/mnt/stor/tmp/" + BACKUP_FILENAME + "/"
SCP_DIR = "/Volumes/External HD/RPi/BACKUPS/"

class Backup:
    # Handles Backup related functions

    def __init__(self, backup_dir=None, backup_filename=None):
        # Backup init handler

        # Set self.backup_dir based on inputs
        if backup_dir is None:
            self.backup_dir = BACKUP_DIR
        else:
            self.backup_dir = backup_dir

        # Set self.backup_filename based on inputs
        if backup_filename is None:
            self.backup_filename = BACKUP_FILENAME
        else:
            self.backup_filename = backup_filename

    def copy(self, path):
        # Copy `path` to backup directory

        if os.path.isdir(path):
            # path is a directory
            try:
                shutil.copytree(path, self.backup_dir)
                success("Backed up " + path)
            except:
                error("Failed backing up " + path)
        else:
            # path is a file
            try:
                shutil.copy2(path, self.backup_dir)
                success("Backed up " + path)
            except:
                error("Failed backing up " + path)

    def archive(self):
        # Archive backup directory
        try:
            shutil.make_archive(self.backup_filename, "zip", self.backup_dir)
            success("Created backup archive.")
        except:
            error("Failed creating backup archive.")

    def send(self, addr, remote_path):
        # Send file to addr:remote_path
        
        try:
            ssh = paramiko.SSHClient()
            ssh.load_system_keys()
            ssh.connect(addr)

            with scp.SCPClient(ssh.get_transport()) as scpc:
                scpc.put(self.backup_filename + ".zip", remote_path + self.backup_filename + ".zip")

            ssh.close()
            success("Sent backup archive to external drive.")
        except:
            error("Failed sending backup archive to external drive.")

    def error(self, msg):
        # Print error message with ornament
        print "! " + msg

    def success(self, msg):
        # Print success message with ornament
        print "✓ " + msg

def main():
    # Main function

    # Create instance of Backup class
    backup = Backup()

    # Tweet that backup is starting
    cur_time = time.strftime("%-I:%M:%S %p")
    tweet.Tweet("@_kylefrost Starting a backup now. The time is " + cur_time + ".")

    try:
        # Things to backup
        # /home
        # /etc/apache2
        # /var/www
        # /etc/crontab
        # pip packages
        # apt packages
        # MySQL databases

        # backup.send("10.0.1.2", "/Volumes/External HD/RPi/BACKUPS/")

        backup.success("Backup was successful.")
        tweet.Tweet("@_kylefrost The backup finished successfully. The backup started at " + cur_time + ".")
    except:
        backup.error("Backup was unsuccessul.")
        tweet.Tweet("@_kylefrost The backup was unsuccessful. The backup started at " + cur_time + ".")
 
if __name__ == "__main__":
    main()
