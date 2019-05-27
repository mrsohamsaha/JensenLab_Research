from opentrons import labware, instruments
from opentrons.data_storage import database

tiprack = labware.load('opentrons-tiprack-300ul', '1')

plate = labware.load('96-flat', '2')
database.delete_container('agar_plate')
plate_agar = labware.create(
        "agar_plate",                    # name of you labware
        grid=(12, 8),                    # specify amount of (columns, rows)
        spacing=(12, 12),               # distances (mm) between each (column, row)
        diameter=6.4,                     # diameter (mm) of each well on the plate
        depth=5,                       # depth (mm) of each well on the plate
        volume=200)

plate2 = labware.load('agar_plate', '5')

pipette = instruments.P300_Single(
	mount = 'right',
	tip_racks = [tiprack])

pipette.pick_up_tip(tiprack.wells('A1'))
pipette.aspirate(20, plate.wells('A1'))
pipette.dispense(20, plate2.wells('A1'))