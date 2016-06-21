import sqlite3
import pyinotify
import datetime

from generaltools import log_tools
from .tools import get_date_taken
PICTURES = "/home/buchbend/scratch/Pictures"
INBOX = "INBOX"
LOG = log_tools.init_logger("monitor_inbox")


class MyEventHandler(pyinotify.ProcessEvent):

    def __init__(self, database):
        self.conn = sqlite3.connect('{}/{}'.format(PICTURES, database))

        self.c = self.conn.cursor()
        try:
            self.c.execute('''CREATE TABLE transferred (file_name text,
            date_taken date, date_transferred date)
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
        date_taken = get_date_taken(event.pathname)
        date_transferred = datetime.datetime.now()
        self.c.execute('''INSERT INTO transferred VALUES (\"{}\", 
        \"{}\", \"{}\")'''.format(event.pathname,
                                  date_taken,
                                  date_transferred))
        print "CREATE event:", event.pathname
        self.conn.commit()

    def process_IN_DELETE(self, event):
        print "DELETE event:", event.pathname

    def process_IN_MODIFY(self, event):
        print "MODIFY event:", event.pathname

    def process_IN_OPEN(self, event):
        print "OPEN event:", event.pathname

def main():
    PICTURES = "/home/buchbend/scratch/Pictures"
    INBOX = "INBOX"
    LOG = log_tools.init_logger("monitor_inbox")

    database = "{}/.uta.db"
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
