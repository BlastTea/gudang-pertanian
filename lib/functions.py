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
        with open(utils.itemsPath):
            pass
    except FileNotFoundError:
        with open(utils.itemsPath, 'w') as openedFile:
            pass
            # df = pd.DataFrame(columns=('id_barang', 'nama_barang', 'tipe_barang', 'harga', 'lama_busuk'))
            # writeDatabase(barangPath, df[df.notna()])

def readDatabase(path) -> pd.DataFrame:
    try:
        dataFrame = pd.read_csv(path)
        return dataFrame
    except:
        pass

def writeDatabase(path:str, dataFrame:pd.DataFrame):
    # with open(path, 'w') as openedFile:
        # return openedFile.write(dataFrame.to_csv('', index=False))
    dataFrame.to_csv(path, index=False)

def printdf(df:pd.DataFrame, *dropColumns):
    if df.index.empty:
        print()
        print('Data masih kosong!'.center(utils.witdh))
        print()
    else:
        for i in dropColumns:
            df.drop(i, inplace=True, axis=1)
        print(tabulate.tabulate(df, headers='keys', tablefmt='psql'))

def getLastIdOf(table:str):
    with open(utils.sharedPreferencesPath) as openedFile:
        data = json.load(openedFile)
        return data[table]

def setLastIdOf(table:str, id:int):
    with open(utils.sharedPreferencesPath) as openedFile:
        data = json.load(openedFile)
        data[table] = id
        openedFile.write(json.dumps(data))

def decodeItemType(x:int) -> str:
    if x == 0:
        return 'sayur'
    elif x == 1:
        return 'buah'
    elif x == 2:
        return 'rumput'
    elif x == 3:
        return 'pupuk'
    elif x == 4:
        return 'bibit'
    else:
        return 'lain-lain'

def encodeItemType():
    pass