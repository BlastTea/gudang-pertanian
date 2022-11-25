import os
import functions
from . import interfaces
import database
import utils
import datetime

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
    
    # racks = database.readRacks(index)
    # return racks['IdRak']
    return index

def itemRackInterface(rackIndex:int) -> int:
    racks = database.readRacks(rackIndex)
    itemRacks = database.readItemRacks(racks['IdRak'])

    while True:
        os.system('cls')
        interfaces.title(racks['Nama'])

        functions.printdf(itemRacks['df'], 'Barang masih kosong!')
        print('1. Masukkan Barang')
        print('2. Keluarkan Barang')
        print('0. Kembali')
        choice = interfaces.getChoice(0, 1, 2)

        if choice != -1:
            return choice

def addItemRackToRackInterface(rackIndex:int):
    items = database.readItems()
    racks = database.readRacks(rackIndex)
    # itemRacks = database.readItemRacks(racks['IdRak'])
    index = 0
    count = 0

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
            count = int(userIn)
        except ValueError:
            input('\nBukan angka!')
            continue

        if count < 1:
            input('\nJumlah harus lebih dari 0')
            continue
    
        break

    database.createItemRack(racks.loc['IdRak'], items.loc[index]['IdBarang'], count)
    
    items = database.readItems()
    # itemRacks = database.readItemRacks(racks['IdRak'])
    items = items.query(f'IdBarang == {items.iloc[index]["IdBarang"]}')

    idItemTransaction = database.createItemTransactionIfNotExists(items['Nama'][index], items['Tipe'][index], items['Harga'][index], items['LamaBusuk'][index])
    idRackTransaction = database.createRackTransactionIfNotExists(racks['Nama'])

    database.createTransaction(idItemTransaction, idRackTransaction, 'Masuk', 'None', count, datetime.datetime.today())
    input('Berhasil ditambahkan!')

def removeItemRackFromRackInterface(rackIndex:int):
    racks = database.readRacks(rackIndex)
    itemRacks = database.readItemRacks(racks['IdRak'])
    index = 0
    count = 0

    os.system('cls')
    interfaces.title('Keluarkan Barang')
    functions.printdf(itemRacks['df'])
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

        if index not in itemRacks['df'].index.values:
            input('\nIndex tidak ada!')
            continue

        break

    selectedStock = itemRacks['df'].loc[index]['Stok']

    while True:
        try:
            userIn = input('\nJumlah yg dikeluarkan : ')
            if userIn == '-':
                return
            count = int(userIn)
        except ValueError:
            input('\nBukan angka!')
            continue

        if count < 1 or selectedStock - count < 0:
            input(f'\nJumlah harus diantara 1 sampai {selectedStock}')
            continue
            
        break

    while True:
        print('\n(Toko, Pasar, Supermarket, Lain-Lain)')
        transactionType = input('Tipe : ')
        if transactionType != 'Lain-Lain':
            transactionType = transactionType.capitalize()
        if transactionType not in ['Toko', 'Pasar', 'Supermarket', 'Lain-Lain']:
            input('\nTipe tidak ada!')
            continue

        break

    items = database.readItems()
    itemRacks = database.readItemRacks(racks['IdRak'])
    items = items.query(f'IdBarang == {items.iloc[index]["IdBarang"]}')

    idItemTransaction = database.createItemTransactionIfNotExists(items['Nama'][index], items['Tipe'][index], items['Harga'][index], items['LamaBusuk'][index])
    idRackTransaction = database.createRackTransactionIfNotExists(racks['Nama'])
    
    database.createTransaction(idItemTransaction, idRackTransaction, 'Keluar', transactionType, count, datetime.datetime.today())
    input('Berhasil dikeluarkan!')

    realStock = selectedStock - count
    if realStock <= 0:
        database.deleteItemRack(index)
    else:
        database.updateItemRack(index, itemRacks['rackIds'][index], itemRacks['itemIds'][index], realStock)
