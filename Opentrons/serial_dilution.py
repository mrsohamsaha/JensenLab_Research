from opentrons import labware, instruments

############### Initialize ###############
tuberack = labware.load('tube-rack-15_50ml', '3')
# plate2 = labware.load('96-deep-well', '3')

plate = labware.load('96-flat', '2')

tiprack = labware.load('opentrons-tiprack-300ul', '1')

# using well plate to mimic agar plate
agar_plate = labware.load('96-flat', '5')

agar_plate = labware.create(
        "agar-plate",                    # name of you labware
        grid=(12, 8),                    # specify amount of (columns, rows)
        spacing=(12, 12),               # distances (mm) between each (column, row)
        diameter=6.4,                     # diameter (mm) of each well on the plate
        depth=1,                       # depth (mm) of each well on the plate
        volume=200)

pipette = instruments.P300_Single(
	mount = 'right',
	tip_racks = [tiprack])

num_dilutions = 4 #1-12
dilution_fold = 10
num_samples = 3 #1-8
well_vol = 50 #microliters

############### Set up ###############
dil_vol = well_vol * (1/dilution_fold)
start_vol = well_vol - dil_vol

# Filling up First Column with inital bacteria solution
pipette.distribute(well_vol, 
					tuberack.wells('A1'), 
					plate.cols['1'][:num_samples])
# pipette.distribute(well_vol, 
# 					plate2.wells('A1'), 
# # 					plate.cols['1'][:num_samples])
# pipette.distribute(dil_vol, 
# 					tuberack.wells('A3'), 
# 					agar_plate.cols['1'][:num_samples])

# Filling up Other Columns with distilled water
for i in range(2, num_dilutions + 1):
	# For now it will fill entire column
	pipette.distribute(start_vol, 
						tuberack.wells('A1'), 
						plate.columns[str(i)][:num_samples])
	# pipette.distribute(start_vol, 
	# 					plate2.wells('A2'), 
	# 					plate.columns[str(i)][:num_samples])

# Dilution and platting
for i in range(num_dilutions - 1): 
	pipette.pick_up_tip()
	for j in range(num_samples):
		well_conversion = i*8 + j
		pipette.transfer(dil_vol, 
						plate.wells(well_conversion), 
						plate.wells(well_conversion + 8), 
						new_tip= 'never')
		pipette.transfer(dil_vol, 
						plate.wells(well_conversion), 
						agar_plate.wells(well_conversion), 
						new_tip= 'never')
	pipette.drop_tip() 
		
