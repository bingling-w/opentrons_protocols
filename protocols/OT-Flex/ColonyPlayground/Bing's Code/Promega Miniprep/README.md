> [!WARNING]
> Working in process, code not tested in actual protocol

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
>[!IMPORTANT]
>Pelleting the bacterial and discarding the supernatant in the 96 deep wellplate must be done manually before starting automated protocol. 

- Before automation, place all labware accordance to the screen visualization set up
- Example Set Up image: <img width="763" height="576" alt="image" src="https://github.com/user-attachments/assets/008d1d9b-a4c6-4573-bd3f-16d4f9b713d3" />
- In deck space A2, place 3 of the stacked collection plate.
- Resuspends, lyses cell and neutralizes the cell.
- Adds Magnesil BLUE and shakes on the shaker.
- Transfers lysate to a collection plate on the magnetic block to clear lysate. Pellets form in this step.
- Adds Magnesil RED into a new binding collection plate, moved from the stack to a new deck using the flex gripper.
- Transfers cleared lysate to binding plate, to mix on the shaker.
- Flex gripper transfers binding plate to magnetic block to form pellets. Supernatant is discarded.
- Binding plate it put pack on the shaker, adding more magnesil RED and clear lysate. Mixed.
- Placed binding plate back on magnetic block to form pellets. Supernatant discarded.
- To wash ethanol is added, shakened, placed on magnetic block to form pellet, and excess liquid is discarded. Repeated twice more.
- Allows plate to dry for 10 minutes.
- Adds elution buffer to the binding plate, mixed and placed back on magnetic block to form pellets.
- Eluate is transferred to a new collection plate, moved from stack to a new deck using the gripper.
- Removes residual particles by placing new collection plate onto the magnetic block to allow pellets to form.
- Transfers the second eluate to a final collection plate to complete protocol. 

## Labware Required (WIP)
This protocol requires the following custom labware:

custom_labware/greiner_96_deep_wellplate_2000ul.json

## Protocol Validations (WIP)
- Validate in Nanodrop

## Protocol Updates
- Ver. 2: Added transfer with liquid class function and flow rate adjustments for small volumes and volatile liquid (80% ethanol)
- Ver. 1: Moved collection plate off deck when no longer needed to save deck space for the rest of the protocol. 
