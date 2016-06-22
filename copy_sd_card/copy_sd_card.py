""" Syncing SD Card to NAS folder
"""
import os
import sqlite3
import subprocess

SD_UUID = "3264-3838"
DESTINATION = "/home/buchbend/scratch/DCIM"

def main():
    if os.path.exists("/tmp/copy_sd"):
        print "unmount copy_sd"
        subprocess.call(["umount", "/tmp/copy_sd"])
    else:
        subprocess.call(["mkdir", "-p", "/tmp/copy_sd"])

    subprocess.call(["mount", "-U", SD_UUID, "/tmp/copy_sd"])
    subprocess.call(["rsync", "-va", "/tmp/copy_sd/DCIM/", DESTINATION])

if __name__ == '__main__':
    main()
