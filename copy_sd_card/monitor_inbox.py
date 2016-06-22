import sqlite3
import pyinotify
import datetime

from generaltools import log_tools
from .tools import get_file_hash

PICTURES = "/home/buchbend/scratch/Pictures"
INBOX = "INBOX"
LOG = log_tools.init_logger("monitor_inbox", "/var/log/monitor_inbox")

FILE_TYPES = ["JPG", "MP4"]

class MyEventHandler(pyinotify.ProcessEvent):

    def __init__(self, database):
        self.conn = sqlite3.connect(database)

        self.c = self.conn.cursor()
        try:
            self.c.execute('''CREATE TABLE transferred (file_name text,
            hash text, date_transferred date)
            ''')
        except sqlite3.OperationalError:
            LOG.debug("Table exists already")


    def process_IN_ACCESS(self, event):
        print "ACCESS event:", event.pathname

    def process_IN_ATTRIB(self, event):
        print "ATTRIB event:", event.pathname

    def process_IN_CLOSE_NOWRITE(self, event):
        print "CLOSE_NOWRITE event:", event.pathname

    def process_IN_CLOSE_WRITE(self, event):
        print "CLOSE_WRITE event:", event.pathname

    def process_IN_CREATE(self, event):
        LOG.debug("CREATE event: {}".format(event.pathname))
        try:
            file_ending = event.pathname.split(".")[-1].upper()
        except:
            LOG.debug("{} Does not seem to be a file".format(event.pathname))
            return 1
        if event.pathname.split(".")[-1].upper() in FILE_TYPES:
            hash_ = get_file_hash(event.pathname)
            date_transferred = datetime.datetime.now()
            self.c.execute('''INSERT INTO transferred VALUES (\"{}\", 
            \"{}\", \"{}\")'''.format(event.pathname,
                                      hash_,
                                      date_transferred))
            self.conn.commit()
            return 0

    def process_IN_DELETE(self, event):
        print "DELETE event:", event.pathname

    def process_IN_MODIFY(self, event):
        print "MODIFY event:", event.pathname

    def process_IN_OPEN(self, event):
        print "OPEN event:", event.pathname

def main():
    database = "{}/.uta.db".format(PICTURES)
    # watch manager
    wm = pyinotify.WatchManager()
    wm.add_watch("{}/{}".format(PICTURES, INBOX),
                 pyinotify.IN_CREATE, rec=True)

    # event handler
    eh = MyEventHandler(database=database)

    # notifier
    notifier = pyinotify.Notifier(wm, eh)
    notifier.loop()

if __name__ == '__main__':
    main()
