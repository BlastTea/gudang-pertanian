import os
import pandas as pd
import tabulate
import utils
import json
import datetime
import numpy as np
import database

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
                utils.tableRacks: 0,
                utils.tableTransactions: 0
            }))
    
    try:
        with open(utils.itemsPath):
            pass
    except FileNotFoundError:
        with open(utils.itemsPath, 'w'):
            items = [
                ['Pisang','Buah',2.0], 
                ['Apel','Buah',7.0], 
                ['Semangka','Buah',21.0],
                ['Jambu Biji','Buah',3.0],
                ['Durian','Buah',18.0],
                ['Tomat','Buah',2.0],
                ['Nanas','Buah',3.0],
                ['Mangga','Buah',3.0],
                ['Naga','Buah',10.0],
            ]

            for i in range(len(items)):
                database.createItem(items[i][0], items[i][1], items[i][2])

    try:
        with open(utils.racksPath):
            pass
    except FileNotFoundError:
        with open(utils.racksPath, 'w'):
            pass
    
    try:
        with open(utils.transactionsPath):
            pass
    except FileNotFoundError:
        with open(utils.transactionsPath, 'w'):
            pass

def readDatabase(path) -> pd.DataFrame | None:
    'fungsi yang digunakan untuk membaca sebuah file csv berdasarkan nama file yang diberikan oleh parameter path, dan mengembalikan dataframe'
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
        print(onEmpty if not onEmpty else 'Data masih kosong!'.center(utils.width))
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
                    jDate = pd.to_datetime(str(j))

                    weekDay = jDate.weekday()
                    day = jDate.day
                    month = jDate.month
                    year = jDate.year

                    hour = jDate.hour
                    minute = jDate.minute
                    second = jDate.second

                    parsedValue.append(f'{getWeekdayIndonesia(weekDay)}, {day} {getMonthIndonesia(month)} {year} {hour}:{minute}:{second}')

                df[i] = parsedValue

        print(tabulate.tabulate(df, headers='keys', tablefmt='psql'))

def getWeekdayIndonesia(weekDay:int) -> str:
    if not 0 <= weekDay <= 6:
        return '?'
    return ['Senin', 'Selasa', 'Rabu', 'Kamis', "Jum'at", 'Sabtu', 'Minggu'][weekDay]

def getMonthIndonesia(month:int) -> str:
    if not 1 <= month <= 12:
        return '?'
    return ['?', 'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'][month]

def getDaysInMonth(year:int, month:int) -> int:
    daysInMonth = [-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if month == 2:
        if year % 4 == 0:
            return 29
        else:
            return 28
    else:
        return daysInMonth[month]

def getDatetimeAt(at:str) -> tuple[datetime.datetime]:
    '''Parameters at
       ----------
       - Today
       - Yesterday
       - ThisWeek
       - ThisMonth
       - ThisYear'''

    now = datetime.datetime.today()
    if at == 'Today':
        return (now, now)
    elif at == 'Yesterday':
        yesterday = now - datetime.timedelta(1)
        return (yesterday, yesterday)
    elif at == 'ThisWeek':
        weekday = now.weekday()
        
        startWeek = weekday
        endWeek = 6 - startWeek

        startDate = now - datetime.timedelta(startWeek)
        endDate = now + datetime.timedelta(endWeek)

        return (startDate, endDate)
    elif at == 'ThisMonth':
        day = now.day
        month = now.month

        startMonth = day - 1
        endMonth = getDaysInMonth(now.year, month) - startMonth - 1

        startDate = now - datetime.timedelta(startMonth)
        endDate = now + datetime.timedelta(endMonth)

        return (startDate, endDate)
    else:
        return (datetime.datetime(now.year, 1, 1), datetime.datetime(now.year, 12, 31))


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