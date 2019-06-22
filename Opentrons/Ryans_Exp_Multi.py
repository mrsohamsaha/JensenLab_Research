from opentrons import labware, instruments

tiprack = labware.load('opentrons-tiprack-300ul', '10')
tiprack1 = labware.load('opentrons-tiprack-300ul', '7')
tiprack2 = labware.load('opentrons-tiprack-300ul', '11')
plate_1 = labware.load('96-flat', '2')
plate_10 = labware.load('96-flat', '5')
plate_100 = labware.load('96-flat', '8')

plate_agar='agar_plate_9_9_9_10'
if plate_agar not in labware.list():
	custom_plate = labware.create(
	        plate_agar,                    # name of you labware
	        grid=(12, 8),                    # specify amount of (columns, rows)
	        spacing=(9, 9),               # distances (mm) between each (column, row)
	        diameter=9,                     # diameter (mm) of each well on the plate
	        depth=10,                       # depth (mm) of each well on the plate
	        volume=200)

agar_plate_1 = labware.load(plate_agar, '3')
agar_plate_10 = labware.load(plate_agar, '4')
agar_plate_100 = labware.load(plate_agar, '9')

dummy = labware.load('96-deep-well', '1')

pipette = instruments.P50_Multi(
	mount = 'left',
	tip_racks = [tiprack, tiprack1, tiprack2])

dil_vol = 10
spot_vol = 7

for i in range(1,12):
	pipette.pick_up_tip()

	pipette.aspirate(spot_vol, dummy.columns(str(i)))
	pipette.aspirate(spot_vol, plate_1.columns(str(i)))
	pipette.dispense(2*spot_vol, agar_plate_1.columns(str(i)))

	pipette.aspirate(dil_vol, dummy.columns(str(i)))
	pipette.aspirate(dil_vol, plate_1.columns(str(i)))
	pipette.dispense(2*dil_vol, plate_10.columns(str(i)))

	pipette.drop_tip()
	pipette.pick_up_tip()

	pipette.aspirate(spot_vol, dummy.columns(str(i)))
	pipette.aspirate(spot_vol, plate_10.columns(str(i)))
	pipette.dispense(2*spot_vol, agar_plate_10.columns(str(i)))

	pipette.aspirate(dil_vol, dummy.columns(str(i)))
	pipette.aspirate(dil_vol, plate_10.columns(str(i)))
	pipette.dispense(2*dil_vol, plate_100.columns(str(i)))

	pipette.drop_tip()
	pipette.pick_up_tip()

	pipette.aspirate(spot_vol, dummy.columns(str(i)))
	pipette.aspirate(spot_vol, plate_100.columns(str(i)))
	pipette.dispense(2*spot_vol, agar_plate_100.columns(str(i)))

	pipette.drop_tip()
	
# for i in range(1,13):
# 	print(plate_1.columns(str(i)))
	# pipette.pick_up_tip()

	# # pipette.aspirate(spot_vol, dummy.columns(str(i)))
	# pipette.consolidate(
	# spot_vol,
	# plate_1.columns(str(i)),
	# agar_plate_1.columns(str(i)),
	# blow_out=True,
	# new_tip='never')

	# pipette.aspirate(dil_vol, dummy.columns(str(i)))
	# pipette.transfer(
	# dil_vol,
	# plate_1.columns(str(i)),
	# plate_10.columns(str(i)),
	# blow_out=True,
	# mix_after=(5,20))

	# pipette.pick_up_tip()

	# pipette.aspirate(spot_vol, dummy.columns(str(i)))
	# pipette.transfer(
	# spot_vol,
	# plate_10.columns(str(i)),
	# agar_plate_10.columns(str(i)),
	# blow_out=True,
	# new_tip='never')

	# pipette.aspirate(dil_vol, dummy.columns(str(i)))
	# pipette.transfer(
	# dil_vol,
	# plate_10.columns(str(i)),
	# plate_100.columns(str(i)),
	# blow_out=True,
	# mix_after=(5,20))

	# pipette.pick_up_tip()

	# pipette.aspirate(spot_vol, dummy.columns(str(i)))
	# pipette.transfer(
	# spot_vol,
	# plate_100.columns(str(i)),
	# agar_plate_100.columns(str(i)),
	# blow_out=True)

