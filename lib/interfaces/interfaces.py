import os
import utils

def title(nama:str):
    print('+', '-' * (utils.witdh - 2), '+')
    print('|', nama.center(utils.witdh - 2), '|')
    print('+', '-' * (utils.witdh - 2), '+')

def getChoice(*choices:int) -> int:
    userInput = 0
    try:
        userInput = int(input('\nPilihan Anda : '))
    except ValueError:
        input('Masukkan angka yang benar!')
        return -1
    else:
        if userInput in choices:
            return userInput
        else:
            input('Pilihan tidak ada!')
            return -1

def mainMenu() -> int:
    while True:
        os.system('cls')
        title('Gudang Pertanian')
        print('1. Rak')
        print('2. Barang')
        print('3. Lihat Detail Rak')
        print('4. Lihat Semua Barang')
        print('5. Laporan')
        print('0. Exit')
        
        choice = getChoice(0, 1, 2, 3, 4, 5)
        if choice != -1:
            return choice