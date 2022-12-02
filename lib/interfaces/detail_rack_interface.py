import os
import functions
from . import interfaces
import database
import utils
import datetime
import time

def detailRackInterface() -> int:
    racks = database.readRacks()
    index = 0

    while True:
        os.system('cls')
        interfaces.title('Detail Rak')
        functions.printdf(racks, dropColumns= ['IdRak'])
        print('\n"-" untuk kembali')

        try:
            userIn = input('\nPilih Index : ')
            if userIn == '-':
                return -1
            index = int(userIn)
        except ValueError:
            input('\nBukan angka!')
            continue
            
        if index not in racks.index.values:
            input('\nIndex tidak ada!')
            continue
            
        break
    return index

def itemRackInterface(rackIndex:int) -> int:
    racks = database.readRacks(rackIndex)
    transactions = database.readTransactions(racks['IdRak'])
    transactions.query('TipeTransaksi == "Masuk"', inplace=True)

    while True: 
        os.system('cls')
        interfaces.title(racks['NamaRak'])

        functions.printdf(transactions[['NamaBarang', 'TipeBarang', 'Jumlah', 'SisaWaktu']], 'Barang masih kosong!')
        print('1. Masukkan Barang')
        print('2. Pindahkan Barang')
        print('3. Keluarkan Barang')
        print('0. Kembali')
        choice = interfaces.getChoice(0, 1, 2, 3)

        if choice != -1:
            return choice

def addItemRackToRackInterface(rackIndex:int):
    items = database.readItems()
    racks = database.readRacks(rackIndex)
    index = 0
    amount = 0

    os.system('cls')
    interfaces.title('Masukkan Barang')
    functions.printdf(items, dropColumns=['IdBarang'])
    print('\n"-" untuk kembali')

    while True:
        try:
            userIn = input('\nPilih index : ')
            if userIn == '-':
                return
            index = int(userIn)
        except ValueError:
            input('\nBukan angka!')
            continue
            
        if index not in items.index.values:
            input('\nIndex tidak ada!')
            continue

        break

    while True:
        try:
            userIn = input('\nJumlah : ')
            if userIn == '-':
                return
            amount = int(userIn)
        except ValueError:
            input('\nBukan angka!')
            continue

        if amount < 1:
            input('\nJumlah harus lebih dari 0')
            continue
    
        break

    database.createTransaction(racks.loc['IdRak'], items.loc[index]['IdBarang'], 'Masuk', amount)

    startedDate = functions.getObject(utils.keyStartedDate)
    if startedDate == None:
        functions.setObject(utils.keyStartedDate, datetime.datetime.today().isoformat())

    input('Berhasil ditambahkan!')

def moveItemRackToAnotherRack(rackIndex:int):
    racks = database.readRacks(rackIndex)
    transactions = database.readTransactions(racks['IdRak'])
    transactions.query('TipeTransaksi == "Masuk"', inplace=True)
    selectedItemIndex = 0
    selectedRackIndex = 0

    while True:
        os.system('cls')
        interfaces.title('Pindahkan Barang')
        functions.printdf(transactions[['NamaBarang', 'TipeBarang', 'Jumlah', 'SisaWaktu']], 'Barang masih kosong!')

        try:
            userIn = input('\nPilih Index Barang : ')
            if userIn == '-':
                return
            selectedItemIndex = int(userIn)
        except ValueError:
            input('\nBukan angka!')
            continue

        if selectedItemIndex not in transactions.index.values:
            input('\nIndex tidak ada!')
            continue

        break

    while True:
        racks2 = database.readRacks()
        os.system('cls')
        interfaces.title('Pindahkan Barang')
        functions.printdf(racks2)

        try:
            userIn = input('\nPilih Index Rak : ')
            if userIn == '-':
                return
            selectedRackIndex = int(userIn)
        except ValueError:
            input('\nBukan angka!')
            continue

        if selectedRackIndex not in racks2.index.values:
            input('\nIndex tidak ada!')
            continue

        break

    item = transactions.loc[selectedItemIndex]
    database.updateTransaction(selectedRackIndex, racks2.loc[selectedRackIndex]['IdRak'], item['IdBarang'], 'Masuk', item['Jumlah'])
    input('Berhasil dipindahkan!')

def removeItemRackFromRackInterface(rackIndex:int):
    racks = database.readRacks(rackIndex)
    transactions = database.readTransactions(racks['IdRak'])
    index = 0
    amount = 0

    os.system('cls')
    interfaces.title('Keluarkan Barang')
    functions.printdf(transactions[['NamaBarang', 'TipeBarang', 'Jumlah', 'SisaWaktu']], 'Barang masih kosong!')
    print('\n"-" untuk kembali')
    
    while True:
        try:
            userIn = input('\nPilih Index : ')
            if userIn == '-':
                return
            index = int(userIn)
        except ValueError:
            input('\nBukan angka!')
            continue

        if index not in transactions.index.values:
            input('\nIndex tidak ada!')
            continue

        break

    # selectedAmount = transactions['df'].loc[index]['Jumlah']

    # while True:
    #     try:
    #         userIn = input('\nJumlah yg dikeluarkan : ')
    #         if userIn == '-':
    #             return
    #         amount = int(userIn)
    #     except ValueError:
    #         input('\nBukan angka!')
    #         continue

    #     if amount < 1 or selectedAmount - amount < 0:
    #         input(f'\nJumlah harus diantara 1 sampai {selectedAmount}')
    #         continue
            
    #     break

    # while True:
    #     print('\n(Toko, Pasar, Supermarket, Lain-Lain)')
    #     transactionType = input('Tipe : ')
    #     if transactionType != 'Lain-Lain':
    #         transactionType = transactionType.capitalize()
    #     if transactionType not in ['Toko', 'Pasar', 'Supermarket', 'Lain-Lain']:
    #         input('\nTipe tidak ada!')
    #         continue

    #     break

    # items = database.readItems()
    # itemRacks = database.readItemRacks(racks['IdRak'])
    # items = items.query(f'IdBarang == {items.iloc[index]["IdBarang"]}')

    # idItemTransaction = database.createItemTransactionIfNotExists(items['Nama'][index], items['Tipe'][index], items['Harga'][index], items['LamaBusuk'][index])
    # idRackTransaction = database.createRackTransactionIfNotExists(racks['Nama'])
    
    # database.createTransaction(idItemTransaction, idRackTransaction, 'Keluar', transactionType, count, datetime.datetime.today())

    # realAmount = selectedAmount - amount
    # if realAmount <= 0:
    database.deleteTransaction(index)
    # else:
    #     database.updateTransaction(index, transactions['rackIds'][index], transactions['itemIds'][index], realAmount)
    input('Berhasil dikeluarkan!')
