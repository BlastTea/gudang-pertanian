import os
import functions
from . import interfaces
import database
import utils
import datetime
import pandas as pd

def allItemInterface():
    os.system('cls')
    interfaces.title('Lihat Semua Barang')

    items = database.readItems()
    racks = database.readRacks()
    transactions = database.readTransactions()

    transactions = transactions.merge(items, on='IdBarang')
    transactions = transactions.merge(racks, on='IdRak')

    longRottens = transactions['LamaBusuk'].values
    incomingDates = transactions['Tanggal'].values

    dayLefts = []

    for i in range(len(longRottens)):
        incomingDate = pd.to_datetime(str(incomingDates[i]))
        ddayRotten = incomingDate.__add__(datetime.timedelta(longRottens[i]))

        dayLeft = ddayRotten - datetime.datetime.today()
        dayLeft = pd.to_timedelta(str(dayLeft))
        dayLefts.append(dayLeft.days)

    transactions['SisaWaktu'] = dayLefts

    transactions = transactions[['NamaRak', 'NamaBarang', 'Tipe', 'SisaWaktu', 'Jumlah']]
    transactions.sort_values(by=['SisaHari'], inplace=True)
    functions.printdf(transactions)

    input()