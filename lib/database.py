import functions
import utils
import pandas as pd
import datetime
import numpy

# Items
def readItems() -> pd.DataFrame:
    'fungsi untuk membaca file "items.csv", mengembalikan dataframe tabel barang'
    items = functions.readDatabase(utils.itemsPath)
    try:
        if items == None:
            items = pd.DataFrame(columns=('IdBarang', 'NamaBarang', 'TipeBarang', 'LamaBusuk'))
    except ValueError:
        if items.empty:
            items = pd.DataFrame(columns=('IdBarang', 'NamaBarang', 'TipeBarang', 'LamaBusuk'))
    items = items.astype({'IdBarang': 'int64', 'NamaBarang': 'string', 'TipeBarang':'string', 'LamaBusuk':'float64'})
    return items

def createItem(name:str, type:str, longRotten:float):
    items = readItems()
    id = functions.getLastIdOf(utils.tableItems) + 1
    functions.setLastIdOf(utils.tableItems, id)
    items.loc[-1] = (id, name, type, longRotten)
    items.sort_values(by=['TipeBarang'], inplace=True)
    functions.writeDatabase(utils.itemsPath, items)

def updateItem(index:int, name:str, type:str, longRotten:float):
    items = readItems()
    items.loc[index] = (items.iloc[index][0], name, type, longRotten)
    items.sort_values(by=['TipeBarang'], inplace=True)
    functions.writeDatabase(utils.itemsPath, items)

def deleteItem(index:int):
    items = readItems()

    itemId = items.iloc[index]['IdBarang']
    transactions = readTransactions()
    transactions.drop(transactions[transactions['IdBarang'] == itemId].index, inplace=True)
    functions.writeDatabase(utils.transactionsPath, transactions)

    items.drop(index, inplace=True)
    items.sort_values(by=['TipeBarang'], inplace=True)
    functions.writeDatabase(utils.itemsPath, items)

# Racks
def readRacks(whereIndex:int = -1) -> pd.DataFrame:
    racks = functions.readDatabase(utils.racksPath)
    try:
        if racks == None:
            racks = pd.DataFrame(columns=('IdRak', 'NamaRak'))
    except ValueError:
        if racks.empty:
            racks = pd.DataFrame(columns=('IdRak', 'NamaRak'))
    racks = racks.astype({'IdRak':'int64', 'NamaRak':'string'})
    if whereIndex != -1:
        racks = racks.loc[whereIndex]
    return racks

def createRack(name:str):
    racks = readRacks()
    id = functions.getLastIdOf(utils.tableRacks) + 1
    functions.setLastIdOf(utils.tableRacks, id)
    racks.loc[-1] = (id, name)
    functions.writeDatabase(utils.racksPath, racks)

def updateRack(index:int, name:str):
    racks = readRacks()
    racks.loc[index] = (racks.iloc[index][0], name)
    functions.writeDatabase(utils.racksPath, racks)

def deleteRack(index:int):
    racks = readRacks()

    rackId = racks.iloc[index]['IdRak']
    transactions = readTransactions()
    transactions.drop(transactions[transactions['IdRak'] == rackId].index, inplace=True)
    functions.writeDatabase(utils.transactionsPath, transactions)

    racks.drop(index, inplace=True)
    functions.writeDatabase(utils.racksPath, racks)

# Transactions
def readTransactions(whereIdRack=-1, merge=True) -> pd.DataFrame:
    timeLefts = []
    items = readItems()
    racks = readRacks()
    transactions = functions.readDatabase(utils.transactionsPath)
    try:
        if transactions == None:
            transactions = pd.DataFrame(columns=('IdTransaksi', 'IdRak', 'IdBarang', 'Jumlah', 'TanggalMasuk', 'TanggalKeluar'))
    except ValueError:
        if transactions.empty:
            transactions = pd.DataFrame(columns=('IdTransaksi', 'IdRak', 'IdBarang', 'Jumlah', 'TanggalMasuk', 'TanggalKeluar'))
    transactions = transactions.astype({'IdTransaksi':'int64', 'IdRak':'int64', 'IdBarang':'int64', 'Jumlah':'int64', 'TanggalMasuk':'datetime64', 'TanggalKeluar':'datetime64[ns]'})

    if whereIdRack != -1:
        transactions.query(f'IdRak == {whereIdRack}', inplace=True)

    if not merge:
        return transactions
        
    transactions = transactions.merge(items, on='IdBarang')
    transactions = transactions.merge(racks, on='IdRak')
    longRottens = transactions['LamaBusuk'].values
    incomingDates = transactions['TanggalMasuk'].values

    if len(longRottens) < 1:
        return transactions

    for i in range(len(longRottens)):
        incomingDate = pd.to_datetime(str(incomingDates[i]))
        ddayRotten = incomingDate.__add__(datetime.timedelta(longRottens[i]))

        timeLeft = ddayRotten - datetime.datetime.today() 
        timeLeft = pd.to_timedelta(str(timeLeft))
        # timeLeft = timedelta.Timedelta(timeLeft)

        dayLeft = timeLeft.days
        hourLeft, remainder = divmod(timeLeft.seconds, 3600)
        minuteLeft, secondLeft = divmod(remainder, 60)
        # secondLeft += timeLeft.microseconds / 1e6

        # dayLeft = timeLeft.total.days
        # hourLeft = timeLeft.total.hours
        # minuteLeft = timeLeft.total.minutes
        # secondLeft = timeLeft.total.seconds

        transactions.at[i, 'SisaHari'] = dayLeft
        transactions.at[i, 'SisaJam'] = hourLeft
        transactions.at[i, 'SisaMenit'] = minuteLeft
        transactions.at[i, 'SisaDetik'] = secondLeft

        finalTimeLeft = ''
        # if dayLeft > 0:
        #     finalTimeLeft = f'{dayLeft} Hari, {hourLeft} Jam'
        # elif hourLeft > 0:
        #     finalTimeLeft = f'{hourLeft} Jam'
        # elif minuteLeft > 0:
        #     finalTimeLeft = f'{minuteLeft} Menit'
        # elif secondLeft > 0:
        #     finalTimeLeft = f'{secondLeft} Detik'
        # else:
        #     finalTimeLeft = '0'
        if timeLeft.seconds <= 0:
            finalTimeLeft = '0'
        else:
            finalTimeLeft = f'{dayLeft}h {hourLeft}j {minuteLeft}m {secondLeft}d'

        timeLefts.append(finalTimeLeft)

    transactions['SisaWaktu'] = timeLefts

    # transactions = transactions[['NamaBarang', 'TipeTransaksi', 'Harga', 'SisaHari', 'Jumlah']]
    transactions.sort_values(by=['SisaHari', 'SisaJam', 'SisaMenit', 'SisaDetik'], ascending=True, inplace=True, ignore_index=True)

    return transactions

def readTransactionByDate(tipe:str, start:datetime.datetime=None, end:datetime.datetime=None) -> pd.DataFrame:
    startDatetime = datetime.datetime(start.year, start.month, start.day, 0, 0, 0)
    endDatetime = datetime.datetime(end.year, end.month, end.day, 23, 59, 59)

    transactions = readTransactions()
    if tipe == 'Masuk':
        transactions.query(f'TanggalKeluar.isnull() & "{startDatetime}" <= TanggalMasuk <= "{endDatetime}"', inplace=True)
        transactions.rename(columns={'TanggalMasuk':'Tanggal'}, inplace=True)
        transactions.drop(columns=['TanggalKeluar'], inplace=True)
        transactions['TipeTransaksi'] = 'Masuk'
    elif tipe == 'Keluar':
        transactions.query(f'"{startDatetime}" <= TanggalKeluar <= "{endDatetime}"', inplace=True)
        transactions.rename(columns={'TanggalKeluar':'Tanggal'}, inplace=True)
        transactions.drop(columns=['TanggalMasuk'], inplace=True)
        transactions['TipeTransaksi'] = 'Keluar'

    return transactions
    
def createTransaction(rackId:int, itemId:int, amount:int):
    transactions = readTransactions(merge=False)
    id = functions.getLastIdOf(utils.tableTransactions) + 1
    functions.setLastIdOf(utils.tableTransactions, id)
    transactions.loc[-1] = (id, rackId, itemId, amount, datetime.datetime.today(), numpy.NaN)
    functions.writeDatabase(utils.transactionsPath, transactions)

def takeTransactionOut(index:int):
    transactions = readTransactions(merge=False)
    id = functions.getLastIdOf(utils.tableTransactions) + 1
    functions.setLastIdOf(utils.tableTransactions, id)
    iloc = transactions.iloc[index]
    transactions.loc[index] = (iloc[0], iloc[1], iloc[2], iloc[3], iloc[4], datetime.datetime.today())
    functions.writeDatabase(utils.transactionsPath, transactions)

def updateTransaction(index:int, rackId:int, itemId:int, amount:int):
    transactions = readTransactions(merge=False)
    transactions.loc[index] = (transactions.iloc[index][0], rackId, itemId, amount, transactions.iloc[index][4], transactions.iloc[index][5])
    functions.writeDatabase(utils.transactionsPath, transactions)

def deleteTransaction(index:int):
    transactions = readTransactions(merge=False)
    transactions.drop(index, inplace=True)
    functions.writeDatabase(utils.transactionsPath, transactions)
    # iloc = transactions.iloc[index]
    # transactions.loc[index] = (iloc[0], iloc[1], iloc[2], 'Keluar', iloc[4], iloc[5])
    # functions.writeDatabase(utils.transactionsPath, transactions)