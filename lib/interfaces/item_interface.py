import os
import functions
from . import interfaces
import database
import utils

def itemInterface() -> int:
    while True:
        os.system('cls')
        interfaces.title('Barang')
        items = database.readItems()
        functions.printdf(items, dropColumns= ['IdBarang'])
        print()
        print('1. Tambah Barang')
        if not items.empty:
            print('2. Edit Barang')
            print('3. Hapus Barang')
        print('0. Kembali')

        choice = -1
        if items.empty:
            choice = interfaces.getChoice(0, 1)
        else:
            choice = interfaces.getChoice(0, 1, 2, 3)

        if choice != -1:
            return choice

def addItemInterface():
    name = ''
    itemType = ''
    price = 0
    longRotten = 0.0

    items = database.readItems()
    os.system('cls')
    interfaces.title('Tambah Barang')

    # while True:
    #     name = input('Nama\t\t\t: ')
    #     if not items.empty:
    #         dfName = items['Nama'].str.contains(name, na=False, case=False)
    #         if dfName.empty:
    #             break
    #         else:
    #             input('\nNama sudah ada!')
    #     else:
    #         break
    name = input('Nama\t\t\t: ')

    while True:
        print('\n(Sayur, Buah, Rumput, Pupuk, Bibit, Lain-Lain)')
        itemType = input('Tipe\t\t\t: ')
        if itemType != 'Lain-Lain':
            itemType = itemType.capitalize()
        if itemType not in ['Sayur', 'Buah', 'Rumput', 'Pupuk', 'Bibit', 'Lain-Lain']:
            input('\nTipe tidak ada!')
            continue
        
        break

    while True:
        try:
            price = int(input('\nHarga\t\t\t: '))
        except ValueError:
            input('\nBukan angka!')
        else:
            break

    while True:
        try:
            longRotten = float(input('\nLama Busuk (Hari)\t: '))
        except ValueError:
            input('\nBukan angka!')
        else:
            break

    database.createItem(name, itemType, price, longRotten)
    input(f'Berhasil ditambahkan!')

def editItemInterface():
    name = ''
    itemType = ''
    price = 0
    longRotten = 0.0

    items = database.readItems()
    index = 0
    while True:
        os.system('cls')
        interfaces.title('Edit Barang')
        functions.printdf(items, dropColumns= ['IdBarang'])
        print('\n"-" untuk kembali')

        try:
            userIn = input('\nPilih Index : ')
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
    
    os.system('cls')
    selectedItem = items.iloc[index]

    interfaces.title('Edit Barang')
    print('Nama\t\t\t: ',selectedItem[1])
    print('Tipe\t\t\t: ',selectedItem[2])
    print('Harga\t\t\t: ',selectedItem[3])
    print('Lama Busuk (Hari)\t: ',selectedItem[4])

    print('-' * utils.witdh)
    print('"-" untuk melewati')

    name = input('Nama\t\t\t: ')
    if name == '-':
        name = selectedItem[1]

    while True:
        print('\n(Sayur, Buah, Rumput, Pupuk, Bibit, Lain-Lain)')
        itemType = input('Tipe\t\t\t: ')
        if itemType == '-':
            itemType = selectedItem[2]
            break
        if itemType != 'Lain-Lain':
            itemType = itemType.capitalize()
        if itemType not in ['Sayur', 'Buah', 'Rumput', 'Pupuk', 'Bibit', 'Lain-Lain']:
            input('\nTipe tidak ada')
        else:
            break
    
    while True:
        try:
            priceInput = input('\nHarga\t\t\t: ')
            if priceInput == '-':
                price = selectedItem[3]
                break
            price = int(priceInput)
        except ValueError:
            input('\nBukan angka!')
        else:
            break

    while True:
        try:
            longRottenInput = input('\nLama Busuk (Hari)\t: ')
            if longRottenInput == '-':
                longRotten = selectedItem[4]
                break
            longRotten = float(longRottenInput)
        except ValueError:
            input('\nBukan angka!')
        else:
            break

    database.updateItem(index, name, itemType, price, longRotten)
    input(f'Berhasil diedit!')

def deleteItemInterface():
    items = database.readItems()
    index = 0

    while True:
        os.system('cls')
        interfaces.title('Hapus Barang')
        functions.printdf(items, dropColumns= ['IdBarang'])
        print('\n"-" untuk kembali')

        try:
            userIn = input('\nPilih Index : ')
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

    database.deleteItem(index)
    input(f'Berhasil dihapus!')