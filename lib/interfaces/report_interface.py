import os
import functions
from . import interfaces
import database
import utils
import datetime

def reportInterface() -> int:
    while True:
        os.system('cls')
        interfaces.title('Laporan')
        database.readTransctions()
        print()
        print('1. Laporan Masuk')
        print('2. Laporan Keluar')
        print('0. Kembali')

        choice = interfaces.getChoice(0, 1, 2)
        if choice != -1:
            return choice

def getDateRangeOfTransaction():
    pass

def incomingReportInterface():
    pass

def outgoingReportInterface():
    pass