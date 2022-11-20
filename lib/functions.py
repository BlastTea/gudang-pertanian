import os
import pandas as pd
import tabulate
import utils


def init():
    if not os.path.exists(utils.databaseFolder):
        os.mkdir(utils.databaseFolder)
    
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

def printdf(df:pd.DataFrame):
    if df.index.empty:
        print()
        print('Data masih kosong!'.center(utils.witdh))
        print()
    else:
        print(tabulate.tabulate(df, headers='keys', tablefmt='psql'))

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