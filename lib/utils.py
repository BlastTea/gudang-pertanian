import os

witdh = 75

tableItems = 'items'
tableRacks = 'racks'
tableTransactions = 'transactions'

databaseFolder = os.path.join(os.getcwd(), 'lib', 'databases')
itemsPath = os.path.join(databaseFolder, f'{tableItems}.csv')
transactionsPath = os.path.join(databaseFolder, f'{tableTransactions}.csv')
racksPath = os.path.join(databaseFolder, f'{tableRacks}.csv')

sharedPreferencesPath = os.path.join(databaseFolder, 'shared_preferences.json')
keyStartedDate = 'started_date'