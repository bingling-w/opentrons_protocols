# WORKING IN PROCESS
# Wizard® MagneSil® Plasmid Purification System (OT-Flex)

## Overview
The protocol performs automated Promega miniprep from the provided 96 collection plate using 
the Opentrons Flex robot with an 1000uL 8-channel. The protocol is 
flexible, allowing inputs for different numbers of wells, up to 96 wells but only in multiples of 8. 

## Protocol Materials
- Robot: Opentrons Flex
- Hardware: Heater shaker with the universal flat plate, magnetic block V1, flex gripper
- Pipette: Flex 8-Channel 1000 uL
- Tips: One 200 uL tip rack and one 1000 uL tip rack
- Plate: Collection plates from the promega miniprep kit
- Reservoir: Opentrons Tough 22 mL 12 Well Reservoir, greiner 96 deep well plate

## Protocol Summary
- Before automation, place all labware accordance to the screen visualization set up
- Example Set Up image: <img width="763" height="576" alt="image" src="https://github.com/user-attachments/assets/008d1d9b-a4c6-4573-bd3f-16d4f9b713d3" />
- In deck space A2, place 3 of the stacked collection plate. 



## Labware Required
This protocol requires the following custom labware:

custom_labware/greiner_96_deep_wellplate_2000ul.json

To be continued

## Protocol Updates
- Ver. 2: Added transfer with liquid class function and flow rate adjustments for small volumes and volatile liquid (80% ethanol)
- Ver. 1: Moved collection plate off deck when no longer needed to save deck space for the rest of the protocol. 
