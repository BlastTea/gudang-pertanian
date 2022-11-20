import os
import functions
from . import interface
import database
import utils

def itemInterface():
    while True:
        os.system('cls')
        interface.title('Barang')
        items = database.readItems()
        functions.printdf(items)
        print()
        print('1. Tambah Barang')
        if not items.empty:
            print('2. Edit Barang')
            print('3. Hapus Barang')
        print('0. Kembali')

        choice = -1
        if items.empty:
            choice = interface.getChoice(0, 1)
        else:
            choice = interface.getChoice(0, 1, 2, 3)

        if choice != -1:
            return choice
            
def addItemInterface():
    name = ''
    type = ''
    price = 0
    longRotten = 0.0

    items = database.readItems()
    os.system('cls')
    interface.title('Tambah Barang')

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
        type = input('Tipe\t\t\t: ')
        type = type.capitalize()
        if type not in ['Sayur', 'Buah', 'Rumput', 'Pupuk', 'Bibit', 'Lain-Lain']:
            input('\nTipe tidak ada')
        else:
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
    
    database.createItem(name, type, price, longRotten)
    input(f'Berhasil ditambahkan!')
            
def editItemInterface():
    name = ''
    type = ''
    price = 0
    longRotten = 0.0

    items = database.readItems()
    index = 0
    while True:
        os.system('cls')
        interface.title('Edit Barang')
        functions.printdf(items)

        try:
           index = int(input('\nPilih Index : '))
        except ValueError:
            input('\nBukan angka!')
            continue
            
        if index not in items.index.values:
            input('\nIndex tidak ada!')
            continue
        
        break
    
    os.system('cls')
    selectedItem = items.iloc[index]

    interface.title('Edit Barang')
    print('Nama\t\t\t: ',selectedItem[0])
    print('Tipe\t\t\t: ',selectedItem[1])
    print('Harga\t\t\t: ',selectedItem[2])
    print('Lama Busuk (Hari)\t: ',selectedItem[3])

    print('-' * utils.witdh)
    print('"-" untuk melewati')

    name = input('Nama\t\t\t: ')
    if name == '-':
        name = selectedItem[0]

    while True:
        print('\n(Sayur, Buah, Rumput, Pupuk, Bibit, Lain-Lain)')
        type = input('Tipe\t\t\t: ')
        if type == '-':
            type = selectedItem[1]
            break
        type = type.capitalize()
        if type not in ['Sayur', 'Buah', 'Rumput', 'Pupuk', 'Bibit', 'Lain-Lain']:
            input('\nTipe tidak ada')
        else:
            break
    
    while True:
        try:
            priceInput = input('\nHarga\t\t\t: ')
            if priceInput == '-':
                price = selectedItem[2]
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
                longRotten = selectedItem[3]
                break
            longRotten = float(longRottenInput)
        except ValueError:
            input('\nBukan angka!')
        else:
            break

    database.updateItem(index, name, type, price, longRotten)
    input(f'Berhasil diedit!')

def deleteItemInterface():
    items = database.readItems()
    index = 0

    while True:
        os.system('cls')
        interface.title('Hapus Barang')
        functions.printdf(items)

        try:
           index = int(input('\nPilih Index : '))
        except ValueError:
            input('\nBukan angka!')
            continue
            
        if index not in items.index.values:
            input('\nIndex tidak ada!')
            continue
        
        break

    database.deleteItem(index)
    input(f'Berhasil dihapus!')