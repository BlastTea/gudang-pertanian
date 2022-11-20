import functions
import utils
import pandas as pd

# Items
def readItems() -> pd.DataFrame:
    items = functions.readDatabase(utils.itemsPath)
    if items.empty:
        items = pd.DataFrame(columns=('Nama', 'Tipe', 'Harga', 'Lama Busuk'))
    items = items.sort_values(by=['Tipe'])
    return items

def createItem(name:str, type:str, price:int, longRotten:float) -> int:
    items = readItems()
    items.loc[-1] = (name, type, price, longRotten)
    items = items.sort_values(by=['Tipe'])
    return functions.writeDatabase(utils.itemsPath, items)

def deleteItem(index:int) -> int:
    items = readItems()
    items = items.drop(index)
    items = items.sort_values(by=['Tipe'])
    return functions.writeDatabase(utils.itemsPath, items)

def updateItem(index:int, name:str, type:str, price:int, longRotten:float) -> int:
    items = readItems()
    items.loc[index] = (name, type, price, longRotten)
    items = items.sort_values(by=['Tipe'])
    return functions.writeDatabase(utils.itemsPath, items)