import os

width = 75
'digunakan untuk lebar dari sebuah judul, maupun lebar garis pada tampilan'

tableItems = 'items'
'variabel global tabel barang'
tableRacks = 'racks'
'variabel global tabel rak'
tableTransactions = 'transactions'
'variabel global tabel transaksi'

databaseFolder = os.path.join(os.getcwd(), 'lib', 'databases')
'path untuk folder databases'
itemsPath = os.path.join(databaseFolder, f'{tableItems}.csv')
'path untuk file items.csv'
racksPath = os.path.join(databaseFolder, f'{tableRacks}.csv')
'path untuk file racks.csv'
transactionsPath = os.path.join(databaseFolder, f'{tableTransactions}.csv')
'path untuk file transactions.csv'

sharedPreferencesPath = os.path.join(databaseFolder, 'shared_preferences.json')
'path untuk sharedPreferences.json, file json ini digunakan untuk menyimpan single variabel'
keyStartedDate = 'started_date'
'key di dalam file sharedPreferences'