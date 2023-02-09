#!/usr/local/bin/python3
import sys, pdb
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

    def writeData(self, file_name=None):
        self.file_name = f'{self.event_name}.txt'

###

# with open('event_list.txt', 'w+b', encoding='utf8'):

ev = CountDownToEvent()
ev.addEvent('정보처리기사 실기')
