import os
import functions
from . import interfaces
import database
import utils

def rackInterface() -> int:
    while True:
        os.system('cls')
        interfaces.title('Rak')
        racks = database.readRacks()
        functions.printdf(racks, 'Id Rak')
        print()
        print('1. Tambah Rak')
        if not racks.empty:
            print('2. Edit Rak')
            print('3. Hapus Rak')
        print('0. Kembali')

        choice = -1
        if racks.empty:
            choice = interfaces.getChoice(0, 1)
        else:
            choice = interfaces.getChoice(0, 1, 2, 3)

        if choice != -1:
            return choice

def addRackInterface():
    name = ''

    racks = database.readRacks()
    os.system('cls')
    interfaces.title('Tambah Rak')

    name = input('Nama\t\t\t: ')
    database.createRacks(name)
    input(f'Berhasil ditambahkan!')

def editRackInterface():
    name = ''

    racks = database.readRacks()
    index = 0
    while True:
        os.system('cls')
        interfaces.title('Edit Rak')
        functions.printdf(racks, 'Id Rak')

        try:
            index = int(input('\nPilih Index : '))
        except ValueError:
            input('\nBukan angka!')
            continue
        
        if index not in racks.index.values:
            input('\nIndex tidak ada!')
            continue
    
        break

    os.system('cls')
    selectedRacks = racks.iloc[index]

    interfaces.title('Edit Rak')
    print('Nama\t\t\t: ', selectedRacks[1])

    print('-' * utils.witdh)
    print('"-" untuk melewati')

    name = input('Nama\t\t\t: ')
    if name == '-':
        name = selectedRacks[1]
        
    database.updateRacks(index, name)
    input('Berhasil diedit!')

def deleteRackInterface():
    racks = database.readRacks()
    index = 0

    while True:
        os.system('cls')
        interfaces.title('Hapus Rak')
        functions.printdf(racks, 'Id Rak')

        try:
            index = int(input('\nPilih Index : '))
        except ValueError:
            input('\nBukan angka!')
            continue
            
        if index not in racks.index.values:
            input('\nIndex tidak ada!')
            continue
            
        break

    database.deleteItem(index)
    input('Berhasil dihapus!')