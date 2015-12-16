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
import sys
import subprocess
import tweet
import keys
import z
import time
import datetime

BACKUP_DIR = ""
BACKUP_FILENAME = ""

###################################################################
#                          BACKUP CLASS                           #
###################################################################

class tcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

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

    def create_backup_dir(self):
        # Handles creating of backup dir

        try:
            # If backup dir exists, delete it
            if os.path.exists(self.backup_dir):
                shutil.rmtree(self.backup_dir)
            
            # Create backup dir
            os.makedirs(self.backup_dir)

            self.success("Backup directory created.")
        except:
            self.error("Could not create backup directory.")
            
    def remove_backup_dir(self):
        # Handles removal of backup dir

        try:
            # If backup dir, delete it
            if os.path.exists(self.backup_dir):
                shutil.rmtree(self.backup_dir)

            self.success("Removed backup directory.")
        except:
            self.error("Could not remove backup directory.")

    def remove_archive_file(self):
        # Removes backup archive zip after sending

        try:
            self.running("Removing backup archive file")
            os.remove(self.backup_filename + ".zip")
            self.success("Removed backup archive file.")
        except:
            self.error("There was a problem removing the archive file.")

    def ignorePath(path):
        def ignoref(p, files):
            return (f for f in files if os.abspath(os.path.join(p, f)) == path)
        return ignoref

    def copy(self, path, bdir):
        # Copy `path` to backup directory

        self.running("Backing up " + path)

        if os.path.isdir(path):
            # path is a directory
            try:
                shutil.copytree(path, self.backup_dir + bdir, symlinks=True)
                self.success("Backed up " + path)
            except:
                self.error("Failed backing up " + path)
        else:
            # path is a file
            try:
                if not os.path.exists(self.backup_dir + bdir):
                    os.makedirs(self.backup_dir + bdir)
                shutil.copy2(path, self.backup_dir + bdir)
                self.success("Backed up " + path)
            except:
                self.error("Failed backing up " + path)

    def archive(self):
        # Archive backup directory
        try:
            self.running("Creating backup archive")
            z.ZipDir(self.backup_dir, self.backup_filename + ".zip")
            self.success("Created backup archive.")
            return True
        except:
            self.error("Failed creating backup archive.")
            return False

    def send(self, addr, remote_path):
        # Send file to addr:remote_path
        
        try:
            self.running("Sending backup zip to remote drive")
            ssh = paramiko.SSHClient()
            ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(addr)

            with scp.SCPClient(ssh.get_transport()) as scpc:
                scpc.put(self.backup_filename + ".zip", remote_path)

            ssh.close()
            self.success("Sent backup archive to external drive.")
        except:
            self.error("Failed sending backup archive to external drive.")

    def error(self, msg):
        # Print error message with ornament
        print tcolors.FAIL + tcolors.UNDERLINE + "! " + msg + tcolors.ENDC + tcolors.ENDC

    def success(self, msg):
        # Print success message with ornament
        print tcolors.OKGREEN + tcolors.BOLD + "✓ " + msg + tcolors.ENDC + tcolors.ENDC

    def running(self, msg):
        print tcolors.OKBLUE + msg + "..." + tcolors.ENDC

    def get_backup_dir(self):
        return self.backup_dir

###################################################################
#                         END BACKUP CLASS                        #
###################################################################

def backup_home(backup):
    # Backup /home

    try:
        backup.copy("/home", "home")
    except:
        pass

def backup_apache(backup):
    # Backup apache2 files

    try:
        def copy_apache(p):
            # Everything in this folder backups to the same place
            if os.path.isdir("/etc/apache2/" + p):
                backup.copy("/etc/apache2/" + p, "etc/apache2/" + p)
            else:
                backup.copy("/etc/apache2/" + p, "etc/apache2")

        copy_apache("apache2.conf")
        copy_apache("conf.d")
        copy_apache("conf-enabled")
        copy_apache("conf-available")
        copy_apache("envvars")
        copy_apache("magic")
        copy_apache("mods-enabled")
        copy_apache("mods-available")
        copy_apache("sites-enabled")
        copy_apache("sites-available")
        copy_apache("ports.conf")
    except:
        pass

def backup_www(backup):
    # Backup /var/www

    try:
        backup.copy("/var/www", "var/www")
    except:
        pass

def backup_crontab(backup):
    # Backup /etc/crontab

    try:
        backup.copy("/etc/crontab", "etc")
    except:
        pass

def backup_pip(backup):
    # Backup pip packages

    try:
        subprocess.call("pip freeze > /tmp/pip.txt", shell=True)
        backup.success("Created /tmp/pip.txt.")
        shutil.copyfile("/tmp/pip.txt", backup.get_backup_dir() + "pip.txt")
        os.remove("/tmp/pip.txt")
        backup.success("Removed /tmp/pip.txt.")
    except:
        backup.error("There was a problem backing up pip packages.")

def backup_apt(backup):
    # Backup apt packages

    # TO REINSTALL
    # sudo dpkg --set-selectins < apt.txt
    # sudo dselect

    try:
        subprocess.call("dpkg --get-selections > /tmp/apt.txt", shell=True)
        backup.success("Created /tmp/apt.txt.")
        shutil.copyfile("/tmp/apt.txt", backup.get_backup_dir() + "apt.txt")
        os.remove("/tmp/apt.txt")
        backup.success("Removed /tmp/apt.txt.")
    except:
        backup.error("There was a problem backing up apt packages.")

def backup_mysql(backup):
    # Backup MySQL databases

    try:
        subprocess.call("mysqldump --all-databases --events -p\"" + keys.MYSQL_PASS + "\" > /tmp/mysql.sql", shell=True)
        backup.success("Created /tmp/mysql.sql.")
        shutil.copyfile("/tmp/mysql.sql", backup.get_backup_dir() + "mysql.sql")
        os.remove("/tmp/mysql.sql")
        backup.success("Removed /tmp/mysql.sql.")
    except:
        backup.error("There was a problem backing up MySQL.")

def backup_mnt(backup):
    # Backup /mnt

    try:
        backup.copy("/mnt/usb", "mnt/usb")

        backup.running("Backing up /mnt/stor")
        subprocess.call("rsync -av /mnt/stor /mnt/stor/tmp " + backup.get_backup_dir() + "/mnt --exclude \"tmp\" > /dev/null", shell=True)
        backup.success("Backed up /mnt/stor.")
    except:
        pass

def get_elapsed(end, start):
    elapsed = end - start
    s = elapsed.seconds
    h, r = divmod(s, 3600)
    m, t = divmod(r, 60)
    return str(h), (str(m) if m > 9 else "0" + str(m)), (str(t) if t > 9 else "0" + str(t))

def main():
    # Main function

    cur_unix_time = str(int(time.time()))
    bfile = "backup" + cur_unix_time
    bdir = "/mnt/stor/tmp/" + bfile + "/"

    # Create instance of Backup class
    backup = Backup(bdir, bfile)

    # Get time for elapsed
    start = datetime.datetime.now()

    # Tweet that backup is starting
    cur_time = time.strftime("%-I:%M:%S %p")
    tweet.Tweet("@_kylefrost Starting a backup now. The time is " + cur_time + ".")

    try:
        # Create backup directory
        backup.create_backup_dir()

        # Backup /home
        backup_home(backup)

        # Backup /etc/apache2 files
        backup_apache(backup)

        # Backup /var/www
        backup_www(backup)

        # Backup /etc/crontab
        backup_crontab(backup)

        # Backup pip packages
        backup_pip(backup)

        # Backup apt packages
        backup_apt(backup)

        # Backup MySQL databases
        backup_mysql(backup)

        # Backup /mnt
        backup_mnt(backup)

        if backup.archive():
            backup.send("10.0.1.2", "/Volumes/External HD/RPi/BACKUPS/")

        backup.remove_backup_dir()
        # backup.remove_archive_file()

        backup.success("Backup was successful.")

        end = datetime.datetime.now()
        hours, minutes, seconds = get_elapsed(end, start)

        tweet.Tweet("@_kylefrost The backup was successful. It started at " + cur_time + ". It took " + hours + "h:" + minutes + "m:" + seconds + "s.")
    except:
        backup.error("Backup was unsuccessul.")

        end = datetime.datetime.now()
        hours, minutes, seconds = get_elapsed(end, start)

        tweet.Tweet("@_kylefrost The backup was unsuccessful. It started at " + cur_time + ". It took " + hours + "h:" + minutes + "m:" + seconds + "s.")
 
if __name__ == "__main__":
    main()
