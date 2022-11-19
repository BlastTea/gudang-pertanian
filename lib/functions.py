import subprocess
import os
import pandas as pd
import tabulate

databaseFolder = os.path.join(os.getcwd(), 'lib', 'databases')
barangPath = os.path.join(databaseFolder, 'barang.csv')

def init():
    if not os.path.exists(databaseFolder):
        os.mkdir(databaseFolder)
    
    try:
        with open(barangPath):
            pass
    except FileNotFoundError:
        with open(barangPath, 'w') as openedFile:
            df = pd.DataFrame(columns=('id_barang', 'nama_barang', 'tipe_barang', 'harga', 'lama_busuk'))
            writeDatabase(barangPath, df[df.notna()])

def readDatabase(path) -> pd.DataFrame:
    try:
        dataFrame = pd.read_csv(path)
        return dataFrame
    except:
        pass

def writeDatabase(path:str, dataFrame:pd.DataFrame) -> int:
    with open(path, 'w') as openedFile:
        return openedFile.write(dataFrame.to_csv(index=False))

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
        print('1. Rak')
        print('2. Barang')
        print('3. Masukkan Barang')
        print('4. Keluarkan Barang')
        print('5. Laporan')
        print('0. Exit')
        
        pilihan = getPilihan(0, 1, 2, 3, 4, 5, 6)
        if pilihan != -1:
            return pilihan

def menuBarang():
    while True:
        os.system('cls')
        judul('Barang')
        print(readDatabase(barangPath))
        print('1. Tambah Barang')
        print('2. Edit Barang')
        print('3. Hapus Barang')
        print('0. Kembali')


        pilihan = getPilihan(0, 1, 2, 3)
        if pilihan == -1:
            continue
            