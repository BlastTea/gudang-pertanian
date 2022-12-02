import functions
from interfaces.interfaces import *
from interfaces.rack_interface import *
from interfaces.item_interface import *
from interfaces.detail_rack_interface import *
from interfaces.report_interface import *
from interfaces.all_item_interface import *

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
        while True:
            detailRackChoice = detailRackInterface()
            
            if detailRackChoice == -1:
                break
            
            while True:
                itemRackChoice = itemRackInterface(detailRackChoice)

                if itemRackChoice == 0:
                    break
                elif itemRackChoice == 1:
                    addItemRackToRackInterface(detailRackChoice)
                elif itemRackChoice == 2:
                    moveItemRackToAnotherRack(detailRackChoice)
                elif itemRackChoice == 3:
                    removeItemRackFromRackInterface(detailRackChoice)
    elif choice == 4:
        allItemInterface()
    elif choice == 5:
        data = {'dateRange' : functions.getDatetimeAt('Today'), 'description':'Hari Ini'}
        sortBy = {'column':'IdTransaksi', 'description':'Id Transaksi'}

        while True:
            data['sortBy'] = sortBy
            reportChoice = reportInterface(data)

            if reportChoice == 1:
                range = changeDateInterface()
                if range != 0:
                    data = range
            elif reportChoice == 2:
                range = sortReportInterface()
                if range != 0:
                    sortBy = range
            else:
                break

    else:
        break
    
