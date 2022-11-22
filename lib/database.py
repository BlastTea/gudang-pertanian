import functions
import utils
import pandas as pd

# Items
def readItems() -> pd.DataFrame:
    items = functions.readDatabase(utils.itemsPath)
    try:
        if items == None:
            items = pd.DataFrame(columns=('Id Barang', 'Nama', 'Tipe', 'Harga', 'Lama Busuk'))
    except ValueError:
        if items.empty:
            items = pd.DataFrame(columns=('Id Barang', 'Nama', 'Tipe', 'Harga', 'Lama Busuk'))
    items = items.sort_values(by=['Tipe'])
    return items

def createItem(name:str, type:str, price:int, longRotten:float):
    items = readItems()
    id = functions.getLastIdOf(utils.tableItems) + 1
    functions.setLastIdOf(utils.tableItems)
    items.loc[-1] = (id, name, type, price, longRotten)
    items = items.sort_values(by=['Tipe'])
    functions.writeDatabase(utils.itemsPath, items)

def updateItem(index:int, name:str, type:str, price:int, longRotten:float):
    items = readItems()
    items.loc[index] = (items.iloc[index][0], name, type, price, longRotten)
    items = items.sort_values(by=['Tipe'])
    functions.writeDatabase(utils.itemsPath, items)

def deleteItem(index:int):
    items = readItems()
    items = items.drop(index)
    items = items.sort_values(by=['Tipe'])
    functions.writeDatabase(utils.itemsPath, items)

# Racks
def readRacks() -> pd.DataFrame:
    racks = functions.readDatabase(utils.racksPath)
    try:
        if racks == None:
            racks = pd.DataFrame(columns=('Id Rak', 'Nama'))
    except ValueError:
        if racks.empty:
            racks = pd.DataFrame(columns=('Id Rak', 'Nama'))
    return racks

def createRacks(name:str):
    racks = readRacks()
    id = functions.getLastIdOf(utils.tableRacks) + 1
    functions.setLastIdOf(utils.tableRacks)
    racks.loc[-1] = (id, name)
    functions.writeDatabase(utils.racksPath, racks)

def updateRacks(index:int, name:str):
    racks = readRacks()
    racks.loc[index] = (racks.iloc[index][0], name)
    functions.writeDatabase(utils.racksPath, racks)

def deleteRacks(index:int):
    racks = readRacks()
    racks = racks.drop(index)
    functions.writeDatabase(utils.racksPath, racks)
