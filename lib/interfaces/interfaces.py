import os
import utils

def title(nama:str):
    print('+', '-' * (utils.witdh - 2), '+')
    print('|', nama.center(48), '|')
    print('+', '-' * (utils.witdh - 2), '+')

def getChoice(*choices) -> int:
    inputan = 0
    try:
        inputan = int(input('\nPilihan Anda : '))
    except ValueError:
        input('Masukkan angka yang benar!')
        return -1
    else:
        if inputan in choices:
            return inputan
        else:
            input('Pilihan tidak ada!')
            return -1

def mainMenu() -> int:
    while True:
        os.system('cls')
        title('Gudang Pertanian')
        print('1. Rak')
        print('2. Barang')
        print('3. Masukkan Barang')
        print('4. Keluarkan Barang')
        print('5. Laporan')
        print('0. Exit')
        
        choice = getChoice(0, 1, 2, 3, 4, 5, 6)
        if choice != -1:
            return choice