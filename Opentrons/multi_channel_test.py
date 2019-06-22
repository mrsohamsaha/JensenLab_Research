from opentrons import labware, instruments

tiprack = labware.load('opentrons-tiprack-300ul', '1')
source = labware.load('96-flat', '2')
# plate = labware.load('96-flat', '5')

plate_agar='agar_plate_9_9_9_10'
if plate_agar not in labware.list():
	custom_plate = labware.create(
	        plate_agar,                    # name of you labware
	        grid=(12, 8),                    # specify amount of (columns, rows)
	        spacing=(9, 9),               # distances (mm) between each (column, row)
	        diameter=9,                     # diameter (mm) of each well on the plate
	        depth=10,                       # depth (mm) of each well on the plate
	        volume=200)

pipette = instruments.P50_Multi(
	mount = 'left',
	tip_racks = [tiprack])

agar_plate_1 = labware.load(plate_agar, '3')

dil_vol = 10
spot_vol = 7


pipette.pick_up_tip()
pipette.aspirate(spot_vol, source.columns('2'))
pipette.aspirate(spot_vol, source.columns('1'))
pipette.dispense(2*spot_vol, agar_plate_1.columns('1'))
# pipette.transfer(
# 	2*spot_vol,
# 	source.columns('1'),
# 	agar_plate_1.columns('1'),
# 	blow_out=True)