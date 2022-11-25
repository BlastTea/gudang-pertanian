import functions
from interfaces.interfaces import *
from interfaces.rack_interface import *
from interfaces.item_interface import *
from interfaces.detail_rack_interface import *

functions.init()

while True:
    choice = mainMenu()

    if choice == 1:
        while True:
            rackChoice = rackInterface()

            if rackChoice == 1:
                addRackInterface()
            elif rackChoice == 2:
                editRackInterface()
            elif rackChoice == 3:
                deleteRackInterface()
            else:
                break
    elif choice == 2:
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
    elif choice == 3:
        # try:
            while True:
                detailRackChoice = detailRackInterface()
                
                if detailRackChoice == -1:
                    raise

            itemRackChoice = itemRackInterface(detailRackChoice)

            if itemRackChoice == 0:
                continue
            elif itemRackChoice == 1:
                    addItemRackToRackInterface(detailRackChoice)
            elif itemRackChoice == 2:
                    removeItemRackFromRackInterface(detailRackChoice)
        # except:
        #     pass

    else:
        break
    
