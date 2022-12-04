import os
import functions
from . import interfaces
import database
import utils
import datetime

def reportInterface(data:dict) -> int:
    transactions = database.readTransactionByDate(data['dateRange'][0], data['dateRange'][1])
    transactions.sort_values(by=[data['sortBy']['column']], ascending=True, inplace=True, ignore_index=True)

    while True:
        os.system('cls')
        interfaces.title(f'Laporan {data["description"]}')
        functions.printdf(transactions[['NamaRak', 'NamaBarang', 'TipeBarang', 'Jumlah', 'TipeTransaksi', 'Tanggal']], indonesiaDate=['Tanggal'])

        if data['sortBy']['column'] != 'IdTransaksi':
            print('-' * utils.width)
            print(f'Disortir berdasarkan {data["sortBy"]["description"]}')
            print('-' * utils.width)

        # print(f'Laporan : {data["dateRange"]}')
        print('1. Ganti Tanggal')
        print('2. Sortir')
        print('0. Kembali')

        choice = interfaces.getChoice(0, 1, 2)
        if choice != -1:
            return choice

def changeDateInterface() -> dict | int:
    while True:
        os.system('cls')
        interfaces.title('Ganti Tanggal')
        print('1. Hari Ini')
        print('2. Kemarin')
        print('3. Minggu ini')
        print('4. Bulan ini')
        print('5. Tahun ini')
        print('0. Kembali')

        choice = interfaces.getChoice(0, 1, 2, 3, 4, 5)
        if choice == 0:
            return choice
        elif choice == -1:
            continue

        at = ['?', 'Today', 'Yesterday', 'ThisWeek', 'ThisMonth', 'ThisYear']
        atI = ['?', 'Hari Ini', 'Kemarin', 'Minggu Ini', 'Bulan Ini', 'Tahun Ini']
        return {'dateRange' : functions.getDatetimeAt(at[choice]), 'description':atI[choice]}

def sortReportInterface() -> dict | int:
    while True:
        os.system('cls')
        interfaces.title('Sortir Berdasarkan')
        print('1. Nama Rak')
        print('2. Nama Barang')
        print('3. Tipe Barang')
        print('4. Jumlah')
        print('5. Tipe Transaksi')
        print('6. Tanggal')
        print('0. Kembali')

        choice = interfaces.getChoice(0, 1, 2, 3, 4, 5, 6)
        if choice == 0:
            return choice
        elif choice == -1:
            continue
        
        return {
            'column': ["NamaRak", "NamaBarang", "TipeBarang", "Jumlah", "TipeTransaksi", "Tanggal"][choice - 1],
            'description': ["Nama Rak", "Nama Barang", "Tipe Barang", "Jumlah", "Tipe Transaksi", "Tanggal"][choice - 1],
        }
        # return ['NamaRak', 'NamaBarang', 'TipeBarang', 'Jumlah', 'TipeTransaksi', 'Tanggal'][choice - 1]