import functions
import utils
import pandas as pd
import datetime

# Items
def readItems() -> pd.DataFrame:
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
def readTransactions(whereIdRack=-1) -> pd.DataFrame:
    timeLefts = []
    items = readItems()
    transactions = functions.readDatabase(utils.transactionsPath)
    try:
        if transactions == None:
            transactions = pd.DataFrame(columns=('IdRakBarang', 'IdRak', 'IdBarang', 'TipeTransaksi' 'Jumlah', 'Tanggal'))
    except ValueError:
        if transactions.empty:
            transactions = pd.DataFrame(columns=('IdRakBarang', 'IdRak', 'IdBarang', 'TipeTransaksi' 'Jumlah', 'Tanggal'))
    transactions = transactions.astype({'IdRakBarang':'int64', 'IdRak':'int64', 'IdBarang':'int64', 'TipeTransaksi':'string', 'Jumlah':'int64', 'Tanggal':'datetime64'})
    if whereIdRack == -1:
        return transactions

    transactions.query(f'IdRak == {whereIdRack}', inplace=True)
    transactions = transactions.merge(items, on='IdBarang')
    longRottens = transactions['LamaBusuk'].values
    incomingDates = transactions['Tanggal'].values

    for i in range(len(longRottens)):
        incomingDate = pd.to_datetime(str(incomingDates[i]))
        ddayRotten = incomingDate.__add__(datetime.timedelta(longRottens[i]))

        timeLeft = ddayRotten - datetime.datetime.today() 
        timeLeft = pd.to_timedelta(str(timeLeft))

        dayLeft = timeLeft.days
        hourLeft = timeLeft.seconds // 60 // 60
        minuteLeft = timeLeft.seconds // 60
        secondLeft = timeLeft.seconds

        transactions.at[i, 'SisaHari'] = dayLeft
        transactions.at[i, 'SisaJam'] = hourLeft
        transactions.at[i, 'SisaMenit'] = minuteLeft
        transactions.at[i, 'SisaDetik'] = secondLeft

        finalTimeLeft = ''
        if dayLeft > 0:
            finalTimeLeft = f'{dayLeft} Hari, {hourLeft} Jam'
        elif hourLeft > 0:
            finalTimeLeft = f'{hourLeft} Jam'
        elif minuteLeft > 0:
            finalTimeLeft = f'{minuteLeft} Menit'
        elif secondLeft > 0:
            finalTimeLeft = f'{secondLeft} Detik'
        else:
            finalTimeLeft = '0'

        timeLefts.append(finalTimeLeft)

    transactions['SisaWaktu'] = timeLefts

    # transactions = transactions[['NamaBarang', 'TipeTransaksi', 'Harga', 'SisaHari', 'Jumlah']]
    transactions.sort_values(by=['SisaHari', 'SisaJam', 'SisaMenit', 'SisaDetik'], ascending=True, inplace=True, ignore_index=True)

    return transactions

def createTransaction(rackId:int, itemId:int, transactionType:str, amount:int):
    transactions = readTransactions()
    id = functions.getLastIdOf(utils.tableTransactions) + 1
    functions.setLastIdOf(utils.tableTransactions, id)
    transactions.loc[-1] = (id, rackId, itemId, transactionType, amount, datetime.datetime.today())
    functions.writeDatabase(utils.transactionsPath, transactions)

def updateTransaction(index:int, rackId:int, itemId:int, transactionType:str, amount:int):
    transactions = readTransactions()
    transactions.loc[index] = (transactions.iloc[index][0], rackId, itemId, transactionType, amount, transactions.iloc[index][5])
    functions.writeDatabase(utils.transactionsPath, transactions)

def deleteTransaction(index:int):
    transactions = readTransactions()
    # transactions.drop(index, inplace=True)
    # functions.writeDatabase(utils.transactionsPath, transactions)
    iloc = transactions.iloc[index]
    transactions.loc[index] = (iloc[0], iloc[1], iloc[2], 'Keluar', iloc[4], iloc[5])
    functions.writeDatabase(utils.transactionsPath, transactions)