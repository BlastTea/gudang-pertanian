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
        print('1. Laporan Barang Masuk')
        print('2. Laporan Barang Keluar')
        print('0. Kembali')

        choice = interfaces.getChoice(0, 1, 2)
        if choice != -1:
            return choice

def getDateRangeOfTransaction() -> tuple[datetime.datetime]:
    pass

def incomingReportInterface():
    incomingTransactions = database.readIncomingTransactions(datetime.datetime.today(), datetime.datetime.today())

    os.system('cls')
    interfaces.title('Laporan Barang Masuk')
    functions.printdf(incomingTransactions, dropColumns=['IdTransaksi', 'IdTransaksiBarang', 'IdTransaksiRak'], indonesiaDate=['Tanggal'])
    input()

def outgoingReportInterface():
    pass