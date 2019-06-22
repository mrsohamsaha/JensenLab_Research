from opentrons import labware, instruments

############### Initialize ###############
source = labware.load('96-deep-well', '3')

plate = labware.load('96-flat', '2')

tiprack = labware.load('opentrons-tiprack-300ul', '1')

plate_agar='agar_plate_9_9_9'
if plate_agar not in labware.list():
	custom_plate = labware.create(
	        plate_agar,                    # name of you labware
	        grid=(12, 8),                    # specify amount of (columns, rows)
	        spacing=(9, 9),               # distances (mm) between each (column, row)
	        diameter=9,                     # diameter (mm) of each well on the plate
	        depth=5,                       # depth (mm) of each well on the plate
	        volume=200)

agar_plate = labware.load(plate_agar, '5')

pipette = instruments.P300_Single(
	mount = 'right',
	tip_racks = [tiprack])

num_dilutions = 4 #1-12
dilution_fold = 5
num_samples = 3 #1-8
well_vol = 100 #microliters

############### Set up ###############
dil_vol = well_vol * (1/dilution_fold)
start_vol = well_vol - dil_vol

# Filling up First Column with inital bacteria solution
pipette.distribute(well_vol, 
					source.wells('A1'), 
					plate.cols['1'][:num_samples])

# Filling up Other Columns with distilled water
for i in range(2, num_dilutions + 1):
	pipette.distribute(start_vol, 
						source.wells('A2'), 
						plate.columns[str(i)][:num_samples])

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
		
