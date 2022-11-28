import os

witdh = 50

tableItems = 'items'
tableTransactions = 'transactions'
tableItemTransactions = 'item_transactions'
tableRackTransactions = 'rack_transactions'
tableRacks = 'racks'
tableItemRacks = 'item_racks'

databaseFolder = os.path.join(os.getcwd(), 'lib', 'databases')
itemsPath = os.path.join(databaseFolder, f'{tableItems}.csv')
transactionsPath = os.path.join(databaseFolder, f'{tableTransactions}.csv')
itemTransactionsPath = os.path.join(databaseFolder, f'{tableItemTransactions}.csv')
rackTransactionsPath = os.path.join(databaseFolder, f'{tableRackTransactions}.csv')
racksPath = os.path.join(databaseFolder, f'{tableRacks}.csv')
itemRacksPath = os.path.join(databaseFolder, f'{tableItemRacks}.csv')

sharedPreferencesPath = os.path.join(databaseFolder, 'shared_preferences.json')
keyStartedDate = 'started_date'