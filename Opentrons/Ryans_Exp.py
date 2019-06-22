from opentrons import labware, instruments

tiprack = labware.load('opentrons-tiprack-300ul', '10')
plate_1 = labware.load('96-deep-well', '2')
plate_10 = labware.load('96-flat', '5')
plate_100 = labware.load('96-flat', '8')

plate_agar='agar_plate_9_9_9'
if plate_agar not in labware.list():
	custom_plate = labware.create(
	        plate_agar,                    # name of you labware
	        grid=(12, 8),                    # specify amount of (columns, rows)
	        spacing=(9, 9),               # distances (mm) between each (column, row)
	        diameter=9,                     # diameter (mm) of each well on the plate
	        depth=5,                       # depth (mm) of each well on the plate
	        volume=200)

agar_plate_1 = labware.load(plate_agar, '3')
agar_plate_10 = labware.load(plate_agar, '4')
agar_plate_100 = labware.load(plate_agar, '9')

pipette = instruments.P300_Single(
	mount = 'right',
	tip_racks = [tiprack])

# 96-well plates are pre-filled
# agar_plate1 has 100 ul of bacteria & media
# agar_plate10 and agar_plate100 have 90ul of media

# Simulating multi-channel with single tip

dil_vol = 30
spot_vol = 30

# Spotting then Dilution
pipette.pick_up_tip()
pipette.transfer(
	spot_vol,
	plate_1.wells('A1'),
	agar_plate_1.wells('A1'),
	blow_out=True,
	new_tip='never')

pipette.transfer(
	dil_vol,
	plate_1.wells('A1'),
	plate_10.wells('A1'),
	blow_out=True,
	touch_tip=True)

pipette.pick_up_tip()
pipette.transfer(
	spot_vol,
	
	plate_10.wells('A1'),
	agar_plate_10.wells('A1'),
	blow_out=True,
	new_tip='never')

pipette.transfer(
	dil_vol,
	plate_10.wells('A1'),
	plate_100.wells('A1'),
	blow_out=True,
	touch_tip=True)

pipette.transfer(
	spot_vol,
	plate_100.wells('A1'),
	agar_plate_100.wells('A1'),
	blow_out=True)





