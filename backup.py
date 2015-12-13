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
import zipfile
import shutil
import os
import tweet
import time

BACKUP_DIR = "/mnt/stor/tmp/backup" + str(int(time.time())) + "/"

class Backup:
    # Handles Backup related functions, i.e. copy, archive, scp

    def __init__(self):
        # Backup init handler

        self.backup_dir = BACKUP_DIR

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
        # Check files, delete oldest if count is = 20
        pass

def main():

    # Things to backup
    # /home
    # /etc/apache2
    # /var/www
    # /etc/crontab
    # pip packages
    # apt packages
    # MySQL databases
 
if __name__ == "__main__":
    main()
