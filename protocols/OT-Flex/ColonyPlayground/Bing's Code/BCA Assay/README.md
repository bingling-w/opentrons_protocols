# Pierce Dilution-Free Rapid Gold BCA Protein Assay Kit (OT-Flex)

## Overview
This protocol performs automated Pierce Gold BCA assay kit from a 96 well plate using the Opentrons Flex robot with an 1000uL 8-channel and 50 uL 1-channel  pipette. The protocol is flexible, allowing inputs for different numbers of BSA unknowns and different numbers of replicates. 

The code can accept up to 24 unknowns for 1 to 2 replicates or accept up to 18 unknowns for 3 replicates.

The Pierce Gold BCA Assay kit itself is for quantification of proteins in an unknown sample. The kit provides 8 standards with known protein concentrations. The unknowns and standards will be mixed with a working reagent (made by mixing reagent A and reagent B), left to incubate for 5 minutes at room temperature, and read in a spectrometry. 

<img width="1160" height="218" alt="image" src="https://github.com/user-attachments/assets/3210d5fc-5c4c-431f-bfea-8e2b65adba7d" />

This is the samples absorbance reading. The standard readings in row 1 will be turned into a linear regression graph. 

<img width="370" height="270" alt="image" src="https://github.com/user-attachments/assets/ec320357-8061-4eb3-afae-40104f85c5c0" />

The quadratic equation y = 0.246x + 0.0249 (y = absorbance) would be used to calculate the unknown protein concentrations in row 2 (x = concentration (mg/mL))

For example, an absorbance of 1.426 means has a protein concentation of 5.696 mg/mL (x = ( y - 0.0249 ) / 0.246)

## Protocol Materials
- Robot: Opentrons Flex
- Hardware: Heater shaker with the universal flat plate
- Pipette: Flex 8-Channel 1000 µL and 1-Channel 50 µL
- Tips: One 200 uL tip rack and one 50 uL tip rack
- Plate: NUNC 96 wellplate optical bottom black
- Reservoir: Opentrons Tough 22 mL 12 Well Reservoir
- Others: Two opentrons 24 tuberack holder

## Protocol Summary
Before automation, place all labware accordance to the screen visualization set up

Example Set Up image for 4 unknowns: <img width="399" height="316" alt="image" src="https://github.com/user-attachments/assets/6ed72e8b-261a-4152-9853-1768faf6d961" />

Red = standards; yellow = unknowns; blue = reagent B; green = reagent A; purple = 50 uL tips;yellow = 200 uL tips. 
1. Place unknowns and standards in preferred order in columns, and dispense the necessary amount of reagent A and B into the reservoir and tube respectively.
2. Start automation protocol.
3. Dispenses 10 µL of BSA standards into column 1 (and column 2-3 if there's replicates)
4. Dispenses 10 µL of BSA unknowns into the column next to the standards (replicates will be placed next to the first replicates row)
5. Combine reagent A and reagent B in a 50:1 ratio, then mix to create the working reagent.
6. Dispense 200 µL of working reagent with the 8-channel pipette into each row where there is standards and unknowns.
7. Heater-shaker will shake the well-plate at 825rpm for 25 seconds to mix well.
8. Protocol will set a timer for 5 minutes.
9. When timer is up, protocol will display completion so user can bring the wellplate to the spectrometry for absorbance reading. 

## Labware Required
This protocol requires the following custom labware:

[custom_labware/nunc_96_wellplate_optical_bottom_400ul.json](https://github.com/bingling-w/opentrons_protocols/blob/4070e261d453abb1e0a81ed08c07d66fa3a36a12/custom_labware/nunc_96_wellplate_optical_bottom_400ul.json)

## Protocol Validations
- $R^2$ value close to 1, signaling strong correlation between absorbance and concentration values. 

## Protocol Updates
- Ver. 9: Code is made to blow out, touch tip, and blow out again to account for viscousity of unknowns and standards to prevent droplets. 
- Ver. 8: Code is optimized to dispense and aspirate slower for more accurate 
- Ver. 7: Code is optimized to use small volume pipette arms and tips to minimize % error of the machine.
- Ver. 6: Code is optimized to use partial nozzle set up for the 8-channel pipette when there is not a full column to reduce WR and tip waste.
- Ver. 5: Code is made so pipette goes to the very bottom of the reservoir to reduce dead volume. 
- Ver. 4: Code is optimized to distribute reagent B uniformly across the reservoir, and mixed with reagent A at different heights for a more uniform mixture. 
- Ver. 2: Code contains mixing and blow out steps, though does not mix as well because the tip can mix max 50 uL volumes. 
- Ver. 1: Code is optimized for flexibility for user to change the protocol base on how many replicates and unknowns is neccessary.
