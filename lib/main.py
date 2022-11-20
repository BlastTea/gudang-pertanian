import functions
from interfaces.interface import *
from interfaces.item_interface import *

functions.init()

while True:
    choice = mainMenu()

    if choice == 2:
        while True:
            itemChoice = itemInterface()
            
            if itemChoice == 1:
                addItemInterface()
            elif itemChoice == 2:
                editItemInterface()
            elif itemChoice == 3:
                deleteItemInterface()
            else:
                break
    else:
        break
    

