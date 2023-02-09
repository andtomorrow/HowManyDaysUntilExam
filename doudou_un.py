#!/usr/local/bin/python3
import os, sys, pdb, datetime
class ForkedPdb(pdb.Pdb):
    """A Pdb subclass that may be used
    from a forked multiprocessing child
    """
    def interaction(self, *args, **kwargs):
        _stdin = sys.stdin
        try:
            sys.stdin = open('/dev/stdin')
            pdb.Pdb.interaction(self, *args, **kwargs)
        finally:
            sys.stdin = _stdin
breakpoint = ForkedPdb().set_trace

class CountDownToEvent:
    def __init__(self):
        self.event_name = ''
        self.days_count = 0
    
    def addEvent(self, event_name):
        self.event_name = event_name
    
    def addDate(self, event_date):
        self.event_date = event_date
        self.date_yy = int(self.event_date[:4])
        self.date_mm = int(self.event_date[4:6])
        self.date_dd = int(self.event_date[-2:])

    def loadFile(self):
        self.event_date = self.f.readline().split('|')[1]
        self.date_yy = int(self.event_date[:4])
        self.date_mm = int(self.event_date[4:6])
        self.date_dd = int(self.event_date[-2:])

    def writeData(self, file_name=None):
        self.file_name = f'{self.event_name}.txt'
        self.f = open(self.file_name, 'w', encoding='utf8')
        self.f.write(f'{self.event_name}|')
        self.f.write(str(self.event_date))

    def inquireEvent(self):
        self.file_name = input('Event name: ')
        self.f = open(f'{self.file_name}.txt', 'r', encoding='utf8')
    
    def requestData(self):
        self.d_day = datetime.date(year=self.date_yy, month=self.date_mm, day=self.date_dd)
        days_delta = abs(datetime.date.today() - self.d_day)
    
        print(days_delta.days, 'days left until', self.event_name)


###

# with open('event_list.txt', encoding='utf8'):
while True:

    os.system('clear')
    usr_input = input("1) Create event \n2) Request D-day count \nAny other input to quit > ")

    if usr_input == '1':
        ev = CountDownToEvent()
        ev.addEvent(input("Event name: "))
        ev.addDate(input("Event date (YYYYMMDD): "))
        ev.writeData("File name before '.txt' (optional): ")
        ev.requestData()
        pas = input('Press enter > ')

    elif usr_input == '2':
        ev = CountDownToEvent()
        ev.inquireEvent()
        ev.loadFile()
        ev.requestData()
        pas = input('Press enter > ')

    else:
        break

    ev.f.close()
