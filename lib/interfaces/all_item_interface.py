import os
import functions
from . import interfaces
import database
import utils
import datetime
import pandas as pd

def allItemInterface():
    os.system('cls')
    interfaces.title('Lihat Semua Barang')
    transactions = database.readTransactions()
    transactions.query('TipeTransaksi == "Masuk"', inplace=True)
    functions.printdf(transactions[['NamaRak', 'NamaBarang', 'TipeBarang', 'Jumlah', 'SisaWaktu']])
    input()