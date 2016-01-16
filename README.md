# backup
Python script for backing up my web server every night.

The script simply dumps all the important stuff into a temporary folder (named `backup` plus the current UNIX timestamp) on a 128GB drive. It organizes it by the folder that the files/directories belong in relation to the root of the file system. It then zips this into an archive and sends it via SCP to a 2TB external drive attached to a different computer on the network. The time this process takes depends entirely on the amount of items found in the backed up directories. The temporary directory and the local archive file are then both removed.

### TODO

- After 50 backups, start deleting oldest in order to keep only 50 at a time.
- Create a restore script that restores these backups (i.e. automates pulling from drive and unarchiving/moving)
- Better error catching and printing
- Break `Backup()` class into separate, reusable module
