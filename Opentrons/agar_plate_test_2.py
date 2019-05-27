from opentrons import labware
from opentrons import instruments
# from opentrons.data_storage import database

tiprack = labware.load('opentrons-tiprack-300ul', '1')

plate = labware.load('96-flat', '2')
#create custom plate if it does not currently exist in robot software
plate_agar='agar_plate_5'
if plate_agar not in labware.list():
	#print('hi')
	custom_plate = labware.create(
	        plate_agar,                    # name of you labware
	        grid=(12, 8),                    # specify amount of (columns, rows)
	        spacing=(8, 8),               # distances (mm) between each (column, row)
	        diameter=8,                     # diameter (mm) of each well on the plate
	        depth=5,                       # depth (mm) of each well on the plate
	        volume=200)

plate2 = labware.load(plate_agar, '5')

pipette = instruments.P300_Single(
	mount = 'right',
	tip_racks = [tiprack])

# Testing single drop
# pipette.pick_up_tip(tiprack.wells('A1'))
# pipette.aspirate(20, plate.wells('A1'))
# pipette.dispense(20, plate2.wells('A1'))

#Testing drops along single column
pipette.transfer(20, 
				plate.wells('A1', 'B1'),
				plate2.wells('A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1'))

# Testing drops along single row
# pipette.transfer(20, 
# 				plate.wells('A1', 'B1', 'C1'),
# 				plate2.wells('A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12'))

