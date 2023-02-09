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
        self.file_name = 'event_data/ev_list.txt'
        self.f = open(self.file_name, 'r', encoding='utf8')
        self.event_lst = self.f.readlines()
        self.events_dct = {self.event_lst[i].split('|')[0]:self.event_lst[i].split('|')[1] for i in range(len(self.event_lst))}
    
    def addEvent(self, event_name):
        self.event_name = event_name
    
    def addDate(self, event_date):
        self.event_date = event_date
        self.date_yy = int(self.event_date[:4])
        self.date_mm = int(self.event_date[4:6])
        self.date_dd = int(self.event_date[-2:])

    def showEvents(self):
        self.ev_num = len(self.event_lst)
        print(f"\n[MESSAGE] You have {self.ev_num} event(s).", "\n----------\n", *self.event_lst, "----------")

    def loadEvent(self):
        while True:
            event_name = input(f"Your events (case-sensitive): ")
            try:
                if event_name in self.events_dct:
                    self.event_name = event_name
                    self.event_date = self.events_dct[event_name]
                    self.date_yy = int(self.event_date[:4])
                    self.date_mm = int(self.event_date[4:6])
                    self.date_dd = int(self.event_date[-2:])
                    break
                elif event_name in 'Qq':
                    break
                else:
                    print("Sorry, invalid event name...")
                    continue
            except:
                continue

    def writeData(self):
        self.f = open(self.file_name, 'a+', encoding='utf8')
        if self.event_name in [self.event_lst[i][0] for i in range(len(self.event_lst))]:
            print(f"Sorry, the event '{self.event_name}' already exists.")
        else:
            self.f.write(f'{self.event_name}|')
            self.f.write(str(f'{self.event_date}\n'))

    def requestData(self):
        self.d_day = datetime.date(year=self.date_yy, month=self.date_mm, day=self.date_dd)
        days_delta = abs(datetime.date.today() - self.d_day)
        os.system('clear')
        print(days_delta.days, 'DAYS LEFT UNTIL', self.event_name, '\nKEEP IT UP!\n----------')


###

while True:

    os.system('clear')
    usr_input = input("1) Create event \n2) Request D-day count \nAny other input to quit > ")

    if usr_input == '1':
        ev = CountDownToEvent()  # create instance
        ev.addEvent(input("Event name: "))
        ev.addDate(input("Event date (YYYYMMDD): "))
        ev.writeData()
        os.system('clear')
        ev.f.close()
        ev.__init__()
        ev.showEvents()
        continu = input('Press enter to continue > ')

    elif usr_input == '2':
        ev = CountDownToEvent()
        os.system('clear')
        ev.showEvents()
        ev.loadEvent()
        if ev.event_name in ev.events_dct:
            ev.requestData()
        else:
            continue
        continu = input('Press enter to continue> ')

    else:
        break

    ev.f.close()
