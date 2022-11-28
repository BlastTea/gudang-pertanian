import os
import pandas as pd
import tabulate
import utils
import json
import datetime
import numpy as np

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
                # utils.tableTransactions: 0,
                # utils.tableItemTransactions: 0,
                # utils.tableRackTransactions: 0,
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
    
    # try:
    #     with open(utils.transactionsPath):
    #         pass
    # except FileNotFoundError:
    #     with open(utils.transactionsPath, 'w'):
    #         pass

    # try:
    #     with open(utils.itemTransactionsPath):
    #         pass
    # except FileNotFoundError:
    #     with open(utils.itemTransactionsPath, 'w'):
    #         pass
    
    # try:
    #     with open(utils.rackTransactionsPath):
    #         pass
    # except FileNotFoundError:
    #     with open(utils.rackTransactionsPath, 'w'):
    #         pass

def readDatabase(path) -> pd.DataFrame:
    try:
        dataFrame = pd.read_csv(path)
        return dataFrame
    except:
        pass

def writeDatabase(path:str, dataFrame:pd.DataFrame):
    dataFrame.to_csv(path, index=False)

def printdf(df:pd.DataFrame, onEmpty:str='Data masih kosong!', dropColumns:list=(), indonesiaDate:list=()):
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

        if len(indonesiaDate) > 0:
            for i in indonesiaDate:
                columnValue:list[np.datetime64] = df[i].values
                parsedValue:list[str] = []
                for j in columnValue:
                    # jDate = j.astype(datetime.datetime)
                    jDate = pd.to_datetime(str(j))

                    weekDay = jDate.weekday()
                    day = jDate.day
                    month = jDate.month
                    year = jDate.year

                    hour = jDate.hour
                    minute = jDate.minute
                    second = jDate.second

                    parsedValue.append(f'{getWeekdayIndonesia(weekDay)}, {day} {getMontIndonesia(month)} {year} {hour}:{minute}:{second}')

                df[i] = parsedValue

        # print(tabulate.tabulate(df, headers='keys', tablefmt='psql'))
        print(tabulate.tabulate(df, headers='keys', tablefmt='psql'))

def getWeekdayIndonesia(weekDay:int) -> str:
    if not 0 <= weekDay <= 6:
        return '?'
    return ['Senin', 'Selasa', 'Rabu', 'Kamis', "Jum'at", 'Sabtu', 'Minggu'][weekDay]

def getMontIndonesia(month:int) -> str:
    if not 1 <= month <= 12:
        return '?'
    return ['?', 'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'][month]

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

def getObject(key:str) -> None | str | int | float | bool:
    with open(utils.sharedPreferencesPath) as openedFile:
        data = json.load(openedFile)
    try:
        data[key]
    except:
        return None
    else: 
        return data[key]

def setObject(key:str, value:str | int | float | bool):
    data = {}
    with open(utils.sharedPreferencesPath) as openedFile:
        data = json.load(openedFile)
        data[key] = value
    with open(utils.sharedPreferencesPath, 'w') as openedFile:
        openedFile.write(json.dumps(data)) 

def getRestRot(date:datetime.datetime, longRotten:float) -> float:
    pass