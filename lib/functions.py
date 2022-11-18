import os

import pandas as pd

databaseFolder = os.path.join(os.getcwd(), 'lib', 'databases')
barangPath = os.path.join(databaseFolder, 'barang.csv')

def init():
    if not os.path.exists(databaseFolder):
        os.mkdir(databaseFolder)
    
    try:
        with open(barangPath):
            pass
    except FileNotFoundError:
        with open(barangPath, 'w'):
            pass

def readDatabase(path:str) -> pd.DataFrame:
    try:
        dataFrame = pd.read_csv(path)
        return dataFrame
    except:
        pass

def judul(nama:str):
    print('+', '-' * 48, '+')
    print('|', nama.center(48), '|')
    print('+', '-' * 48, '+')

def getPilihan(*pilihan) -> int:
    inputan = 0
    try:
        inputan = int(input('\nPilihan Anda : '))
    except ValueError:
        input('Masukkan angka yang benar!')
        return -1
    else:
        if inputan in pilihan:
            return inputan
        else:
            input('Pilihan tidak ada!')
            return -1


def menuUtama() -> int:
    while True:
        os.system('cls')
        judul('Gudang Pertanian')
        print('1. Barang')
        print('0. Exit')
        
        pilihan = getPilihan(0, 1)
        if pilihan != -1:
            return pilihan

def menuBarang():
    while True:
        os.system('cls')
        judul('Barang')
        readDatabase(barangPath)
        print('1. Tambah Barang')
        print('2. Edit Barang')
        print('3. Hapus Barang')
        print('0. Kembali')

        pilihan = getPilihan(0, 1, 2, 3)
        if pilihan == -1:
            continue
            
        
    
