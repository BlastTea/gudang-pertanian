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

        # print()
        # print('1. Tambah Barang')
        # if not items.empty:
        #     print('2. Edit Barang')
        #     print('3. Hapus Barang')
        # print('0. Kembali')

        # choice = -1
        # if items.empty:
        #     choice = interfaces.getChoice(0, 1)
        # else:
        #     choice = interfaces.getChoice(0, 1, 2, 3)

        # if choice != -1:
        #     return choice
        input()
        return 0

def addItemInterface():
    name = ''
    itemType = ''
    longRotten = 0.0

    os.system('cls')
    interfaces.title('Tambah Barang')
    while True:
        name = input('Nama\t\t\t: ').strip()

        if not name:
            input('Nama masih kosong!')
            continue

        break

    while True:
        print('\n(Sayur, Buah)')
        itemType = input('Tipe\t\t\t: ').strip()
        if itemType != 'Lain-Lain':
            itemType = itemType.capitalize()
        if itemType not in ['Sayur', 'Buah']:
            input('\nTipe tidak ada!')
            continue
        
        break

    while True:
        try:
            longRotten = float(input('\nLama Busuk (Hari)\t: '))
        except ValueError:
            input('\nBukan angka!')
        else:
            break

    database.createItem(name, itemType, longRotten)
    input(f'Berhasil ditambahkan!')

def editItemInterface():
    name = ''
    itemType = ''
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
    print('Lama Busuk (Hari)\t: ',selectedItem[4])

    print('-' * utils.witdh)
    print('"-" untuk melewati')

    while True:
        name = input('Nama\t\t\t: ').strip()

        if not name:
            input('Nama masih kosong!')
            continue

        break
    
    if name == '-':
        name = selectedItem[1]

    while True:
        print('\n(Sayur, Buah)')
        itemType = input('Tipe\t\t\t: ').strip()
        if itemType == '-':
            itemType = selectedItem[2]
            break
        if itemType != 'Lain-Lain':
            itemType = itemType.capitalize()
        if itemType not in ['Sayur', 'Buah']:
            input('\nTipe tidak ada')
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

    database.updateItem(index, name, itemType, longRotten)
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