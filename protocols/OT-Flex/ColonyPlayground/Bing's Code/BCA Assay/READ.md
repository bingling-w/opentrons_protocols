# Pierce Dilution-Free Rapid Gold BCA Protein Assay Kit (OT-Flex)

## Overview
The protocol performs automated Pierce Gold BCA assay kit from a 96 well plate using the Opentrons Flex robot with an 1000uL 8-channel and 50 uL 1-channel  pipette. The protocol is flexible, allowing inputs for different numbers of BSA unknowns and different numbers of replicates. 

The code can accept up to 24 unknowns for 1 to 2 replicates
Or accept up to 18 unknowns of 3 replicates.

## Protocol Materials
- Robot: Opentrons Flex
- Hardware: Heater shaker with the universal flat plate
- Pipette: Flex 8-Channel 1000 µL and 1-Channel 50 µL
- Tips: One 200 uL tip rack and one 50 uL tip rack
- Plate: NUNC 96 wellplate optical bottom black
- Reservoir: Opentrons Tough 22 mL 12 Well Reservoir
- Others: Two opentrons 24 tuberack holder

## Protocol Summary
- Before automation, place all labware accordance to the screen visualization set up
- Example Set Up image: <img width="399" height="316" alt="image" src="https://github.com/user-attachments/assets/6ed72e8b-261a-4152-9853-1768faf6d961" />
- Place unknowns and standards in preferred pattern, and dispense the necessary amount of reagent A and B into the reservoir and tube respectively.
- Start automation protocol.
- Dispenses 10 µL of BSA standards into column 1 (and column 2-3 if there's replicates)
- Dispense 10 µL of BSA unknowns into the column next to the standards (replicates will be placed next to the first replicates row)
- Mix reagent a and reagent b to create the working reagent
- Dispense 200 µL with the 8-channel pipette into each row where there is standards and unknowns.
- Heater-shaker will shake the well-plate at 825rpm for 20 seconds.
- Protocol complete, protocol will set a timer for when to put the well plate to the spectrometry

## Labware Required
This protocol requires the following custom labware:

custom_labware/nunc_96_wellplate_optical_bottom_400ul.json
