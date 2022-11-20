import os

witdh = 50

databaseFolder = os.path.join(os.getcwd(), 'lib', 'databases')
racksPath = os.path.join(databaseFolder, 'racks.csv')
itemRacksPath = os.path.join(databaseFolder, 'item_racks.csv')
itemsPath = os.path.join(databaseFolder, 'items.csv')
outgoingTransactionsPath = os.path.join(databaseFolder, 'outgoing_transactions.csv')
incomingTransactionsPath = os.path.join(databaseFolder, 'incoming_transactions.csv')