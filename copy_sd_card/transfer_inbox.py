import os
import sqlite3
import glob
import datetime
import subprocess

from PIL import Image
from generaltools import log_tools

def get_date_taken(path):
    return Image.open(path)._getexif()[36867]

LOG = log_tools.init_logger("transfer_inbox")

SOURCE = "/home/buchbend/scratch/DCIM/"
INBOX = "/home/buchbend/scratch/INBOX/"

def check_if_transferred(path, date_taken, cursor):
    cursor.execute('''SELECT * FROM transferred
    WHERE file_name=\"{}\" and
    date_taken=\"{}\"'''.format(path, date_taken))
    try:
        cursor.fetchone()[0]
        return True
    except TypeError:
        return False

conn = sqlite3.connect('transfer.db')

c = conn.cursor()


try:
    c.execute('''CREATE TABLE transferred (file_name text,
    date_taken date, date_transferred date)
    ''')
except sqlite3.OperationalError:
    LOG.debug("Table exists already")



file_list = []
for path, subdirs, files in os.walk(SOURCE):
    files = [f for f in files if "JPG" in f]
    for name in files:
        file_list += [os.path.join(path, name)]

for this_path in file_list:
    date_taken = get_date_taken(this_path)
    date_transferred = datetime.datetime.now()
    transferred = check_if_transferred(this_path, date_taken, c)
    if not transferred:
        LOG.debug("Copy {} to {}".format(this_path, INBOX))
        subprocess.call(["cp", "-a", this_path, INBOX])
        c.execute("INSERT INTO transferred VALUES (\"{}\", \"{}\", \"{}\")".format(this_path, date_taken, date_transferred))

conn.commit()
conn.close()
