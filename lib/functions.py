import os
import pandas as pd
import tabulate
import utils
import json

def init():
    if not os.path.exists(utils.databaseFolder):
        os.mkdir(utils.databaseFolder)

    try:
        with open(utils.sharedPreferencesPath):
            pass
    except FileNotFoundError:
        with open(utils.sharedPreferencesPath, 'w') as openedFile:
            openedFile.write(json.dumps({
                utils.tableItems: 0,
                utils.tableTransactions: 0,
                utils.tableItemTransactions: 0,
                utils.tableRacks: 0,
                utils.tableItemRacks: 0
            }))
    
    try:
        with open(utils.racksPath):
            pass
    except FileNotFoundError:
        with open(utils.racksPath, 'w'):
            pass

    try:
        with open(utils.itemsPath):
            pass
    except FileNotFoundError:
        with open(utils.itemsPath, 'w'):
            pass
    
    try:
        with open(utils.itemRacksPath):
            pass
    except FileNotFoundError:
        with open(utils.itemRacksPath, 'w'):
            pass
    
    try:
        with open(utils.transactionsPath):
            pass
    except FileNotFoundError:
        with open(utils.transactionsPath, 'w'):
            pass
    

def readDatabase(path) -> pd.DataFrame:
    try:
        dataFrame = pd.read_csv(path)
        return dataFrame
    except:
        pass

def writeDatabase(path:str, dataFrame:pd.DataFrame):
    dataFrame.to_csv(path, index=False)

def printdf(df:pd.DataFrame, onEmpty:str='Data masih kosong!', dropColumns:list=()):
    if df.index.empty:
        print()
        print(onEmpty if not onEmpty else 'Data masih kosong!'.center(utils.witdh))
        print()
    else:
        df = df.copy()

        if len(dropColumns) > 0:
            for i in dropColumns:
                df.drop(i, inplace=True, axis=1)
        elif len(dropColumns) == 1:
            df.drop(dropColumns, inplace=True, axis=1)
        # print(tabulate.tabulate(df, headers='keys', tablefmt='psql'))
        print(tabulate.tabulate(df, headers='keys', tablefmt='psql'))

def getLastIdOf(table:str):
    with open(utils.sharedPreferencesPath) as openedFile:
        data = json.load(openedFile)
        return data[table]

def setLastIdOf(table:str, id:int):
    data = {}
    with open(utils.sharedPreferencesPath) as openedFile:
        data = json.load(openedFile)
        data[table] = id
    with open(utils.sharedPreferencesPath, 'w') as openedFile:
        openedFile.write(json.dumps(data))