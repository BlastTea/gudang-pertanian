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
    itemRacks = database.readItemRacks()

    itemRacks = itemRacks.merge(items, on='IdBarang')
    itemRacks = itemRacks.merge(racks, on='IdRak')

    longRottens = itemRacks['LamaBusuk'].values
    incomingDates = itemRacks['TanggalMasuk'].values

    dayLefts = []

    for i in range(len(longRottens)):
        incomingDate = pd.to_datetime(str(incomingDates[i]))
        ddayRotten = incomingDate.__add__(datetime.timedelta(longRottens[i]))

        dayLeft = ddayRotten - incomingDate
        dayLeft = pd.to_timedelta(str(dayLeft))
        dayLefts.append(dayLeft.days)

    itemRacks['SisaHari'] = dayLefts

    itemRacks = itemRacks[['NamaRak', 'NamaBarang', 'Tipe', 'Harga', 'SisaHari', 'Jumlah']]
    itemRacks.sort_values(by=['SisaHari'], inplace=True)
    functions.printdf(itemRacks)

    input()