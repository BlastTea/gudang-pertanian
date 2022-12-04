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
        functions.printdf(racks, dropColumns= ['IdRak'])
        print()
        print('1. Tambah Rak')
        if not racks.empty:
            print('2. Edit Rak')
        print('0. Kembali')

        choice = -1
        if racks.empty:
            choice = interfaces.getChoice(0, 1)
        else:
            choice = interfaces.getChoice(0, 1, 2)

        if choice != -1:
            return choice

def addRackInterface():
    name = ''


    while True:
        os.system('cls')
        interfaces.title('Tambah Rak')
        print('\n"-" untuk kembali')
        name = input('\nNama\t\t\t: ').strip()
        if name == '-':
            return

        if not name:
            input('Nama masih kosong!')
            continue

        break

    database.createRack(name)
    input(f'Berhasil ditambahkan!')

def editRackInterface():
    name = ''

    racks = database.readRacks()
    index = 0
    while True:
        os.system('cls')
        interfaces.title('Edit Rak')
        functions.printdf(racks, dropColumns= ['IdRak'])
        print('\n"-" untuk kembali')

        try:
            userIn = input('\nPilih Index : ')
            if userIn == '-':
                return
            index = int(userIn)
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

    print('-' * utils.width)
    print('"-" untuk melewati')

    while True:
        name = input('Nama\t\t\t: ').strip()

        if not name:
            input('Nama masih kosong!')
            continue

        break
    
    if name == '-':
        name = selectedRacks[1]
        
    database.updateRack(index, name)
    input('Berhasil diedit!')

def deleteRackInterface():
    racks = database.readRacks()
    index = 0

    while True:
        os.system('cls')
        interfaces.title('Hapus Rak')
        functions.printdf(racks, dropColumns= ['IdRak'])
        print('\n"-" untuk kembali')

        try:
            userIn = input('\nPilih Index : ')
            if userIn == '-':
                return
            index = int(userIn)
        except ValueError:
            input('\nBukan angka!')
            continue
            
        if index not in racks.index.values:
            input('\nIndex tidak ada!')
            continue
            
        break

    database.deleteRack(index)
    input('Berhasil dihapus!')