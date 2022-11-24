import functions
import utils
import pandas as pd

# Items
def readItems() -> pd.DataFrame:
    items = functions.readDatabase(utils.itemsPath)
    try:
        if items == None:
            items = pd.DataFrame(columns=('IdBarang', 'Nama', 'Tipe', 'Harga', 'LamaBusuk'))
    except ValueError:
        if items.empty:
            items = pd.DataFrame(columns=('IdBarang', 'Nama', 'Tipe', 'Harga', 'LamaBusuk'))
    items.sort_values(by=['Tipe'], inplace=True)
    return items

def createItem(name:str, type:str, price:int, longRotten:float):
    items = readItems()
    id = functions.getLastIdOf(utils.tableItems) + 1
    functions.setLastIdOf(utils.tableItems, id)
    items.loc[-1] = (id, name, type, price, longRotten)
    items.sort_values(by=['Tipe'], inplace=True)
    functions.writeDatabase(utils.itemsPath, items)

def updateItem(index:int, name:str, type:str, price:int, longRotten:float):
    items = readItems()
    items.loc[index] = (items.iloc[index][0], name, type, price, longRotten)
    items.sort_values(by=['Tipe'], inplace=True)
    functions.writeDatabase(utils.itemsPath, items)

def deleteItem(index:int):
    items = readItems()
    items.drop(index, inplace=True)
    items.sort_values(by=['Tipe'], inplace=True)
    functions.writeDatabase(utils.itemsPath, items)

# Racks
def readRacks(whereIndex:int = -1) -> pd.DataFrame:
    racks = functions.readDatabase(utils.racksPath)
    try:
        if racks == None:
            racks = pd.DataFrame(columns=('IdRak', 'Nama'))
    except ValueError:
        if racks.empty:
            racks = pd.DataFrame(columns=('IdRak', 'Nama'))
    if whereIndex != -1:
        racks = racks.loc[whereIndex]
    return racks

def createRack(name:str):
    racks = readRacks()
    id = functions.getLastIdOf(utils.tableRacks) + 1
    functions.setLastIdOf(utils.tableRacks, id)
    racks.loc[-1] = (id, name)
    functions.writeDatabase(utils.racksPath, racks)

def updateRack(index:int, name:str):
    racks = readRacks()
    racks.loc[index] = (racks.iloc[index][0], name)
    functions.writeDatabase(utils.racksPath, racks)

def deleteRack(index:int):
    racks = readRacks()
    racks.drop(index, inplace=True)
    functions.writeDatabase(utils.racksPath, racks)

# ItemRacks
def readItemRacks(idRacks:int = -1) -> pd.DataFrame | dict:

    itemRacks = functions.readDatabase(utils.itemRacksPath)
    try:
        if itemRacks == None:
            itemRacks = pd.DataFrame(columns=('IdRakBarang', 'IdRak', 'IdBarang', 'Stok'))
    except ValueError:
        if itemRacks.empty:
            itemRacks = pd.DataFrame(columns=('IdRakBarang', 'IdRak', 'IdBarang', 'Stok'))
    if idRacks == -1:
        return itemRacks
    itemRackIds = itemRacks['IdRakBarang'].values
    rackIds = itemRacks['IdRak'].values
    itemIds = itemRacks['IdBarang'].values

    itemRacks.query(f'IdRak == {idRacks}', inplace=True)
    itemRacks.drop('IdRak', inplace=True, axis=1)
    itemRacks.drop('IdRakBarang', inplace=True, axis=1)

    items = readItems()

    itemRacks = itemRacks.merge(items, how='left', on='IdBarang')
    itemRacks.drop('IdBarang', inplace=True, axis=1)
    itemRacks = itemRacks[['Nama', 'Tipe', 'Harga', 'LamaBusuk', 'Stok']]

    return {'df': itemRacks, 'itemRackIds': itemRackIds, 'rackIds': rackIds, 'itemIds': itemIds}

def createItemRack(idRack:int, idItem:int, stock:int):
    itemRacks = readItemRacks()
    id = functions.getLastIdOf(utils.tableItemRacks) + 1
    functions.setLastIdOf(utils.tableItemRacks, id)
    itemRacks.loc[-1] = (id, idRack, idItem, stock)
    functions.writeDatabase(utils.itemRacksPath, itemRacks)

def updateItemRack(index:int, idRack:int, idItem:int, stock:int):
    itemRacks = readItemRacks()
    itemRacks.loc[index] = (itemRacks.iloc[index][0], idRack, idItem, stock)
    functions.writeDatabase(utils.itemRacksPath, itemRacks)

def deleteItemRack(index:int):
    itemRacks = readItemRacks()
    itemRacks.drop(index, inplace=True)
    functions.writeDatabase(utils.itemRacksPath, itemRacks)

def readTransctions() -> pd.DataFrame:
    transactions = functions.readDatabase(utils.transactionsPath)
    # try:
    #     if transactions == None:
    #         transactions = pd.DataFrame(columns=('IdTransaksi', 'IdTransaksiBarang', 'IdRakBarang', 'Tipe'))