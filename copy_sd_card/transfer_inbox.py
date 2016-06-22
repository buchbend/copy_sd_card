import os
import sqlite3
import glob
import datetime
import subprocess
import hashlib

from .tools import get_file_hash
from generaltools import log_tools

LOG = log_tools.init_logger("transfer_inbox")

SOURCE = "/home/buchbend/scratch/DCIM/"
PICTURES = "/home/buchbend/scratch/Pictures/"
INBOX = "INBOX"

DATABASE = ".transfer.db"
EXTERNAL_DATABASES = [".transfer_uta.db", ".transfer_christof.db"]

FILE_TYPES = ["JPG", "MP4", "AVI"]

def connect_to_database(database):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    return conn, c

def check_if_transferred(path, hash_, cursor):
    cursor.execute('''SELECT * FROM transferred
    WHERE file_name=\"{}\" and
    hash=\"{}\"'''.format(path, hash_))
    try:
        cursor.fetchone()[0]
        return True
    except TypeError:
        return False

def main():

    # Connect to the central database
    database = "{}/{}".format(PICTURES, DATABASE)
    try:
        conn, c = connect_to_database(database=database)
    except:
        raise SystemExit("Can not connect to {}".format(database))
    try:
        c.execute('''CREATE TABLE transferred (file_name text,
        hash text, date_transferred date)
        ''')
    except sqlite3.OperationalError:
        LOG.debug("Table exists already")

    # Connect to possible external databases
    ext_databases = []
    for database in EXTERNAL_DATABASES:
        database = "{}/{}".format(PICTURES, database)
        conn_, c_ = connect_to_database(database)
        ext_databases += [c]

    # Get all files from the input folder
    file_list = []
    for path, subdirs, files in os.walk(SOURCE):
        files = [f for f in files if f.split(".")[-1] in FILE_TYPES]
        for name in files:
            file_list += [os.path.join(path, name)]

    # Loop over all files and copy them to the INBOX if they have not been
    # copied before
    for this_path in file_list:
        date_transferred = datetime.datetime.now()
        hash_ = get_file_hash(this_path)
        transferred = check_if_transferred(this_path, hash_, c)
        if not transferred:
            LOG.debug("Copy {} to {}".format(this_path, INBOX))
            subprocess.call(["cp", "-a", this_path, INBOX])
            c.execute("""INSERT INTO transferred VALUES
        (\"{}\", \"{}\", \"{}\")""".format(this_path,
                                           hash_,
                                           date_transferred))

    # Close the database
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
