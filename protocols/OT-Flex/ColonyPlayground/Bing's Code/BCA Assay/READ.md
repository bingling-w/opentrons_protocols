# Pierce Dilution-Free Rapid Gold BCA Protein Assay Kit (OT-Flex)

## Overview
The protocol performs automated BCA assay kit from a 96 well plate using the Opentrons Flex robot with an 8-channel and 1-channel 1000 µL pipette. The protocol is flexible, allowing inputs for different numbers of BSA unknowns and different numbers of replicates. 

The code can accept up to 23 unknowns for 1 to 2 replicates
Or accept up to 18 unknowns if 3 replicates.

## Protocol Summary
- Robot: Opentrons Flex
- Pipette: Flex 8-Channel 1000 µL and 1-Channel 1000 µL
- Plate: NUNC 96 wellplate optical bottom black 400 µL
- Before automation, dispense approximately 30-40 µL into column 1 of the well plate, and place onto the heater shaker. 
- Dispense 10 µL of BSA standards into column 2 (and column 3-4 if there's replicates)
- Dispense 10 µL of BSA unknowns into the column next to the standards (replicates will be placed next to the first replicates row)
- Mix reagent a and reagent b to create the working reagent
- Dispense 200 µL with the 8-channel pipette into each row where there is standards and unknowns (even if there is only one filled well in a column)
- Heater-shaker will shake the well-plate at 900rpm for 20 seconds.
- Protocol complete, protocol will set a timer for when to put the well plate to the spectrometry

## Labware Required
This protocol requires the following custom labware:

custom_labware/nunc_96_wellplate_optical_bottom_400ul.json
