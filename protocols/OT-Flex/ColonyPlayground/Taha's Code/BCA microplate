from opentrons import protocol_api
from opentrons.types import Point

# Initial conditions
# 8 Standards in tube rack first two columns
# Up to 12 unknowns in tube rack columns 3-5 starting in row A and working down (A3, B3 ,... ,D5)
# Reagent A in reservoir slot 1
# Reagent B in tube rack top right corner
# Replication between 1-4

# WR preparation volumes
num_std = 8  # Stock standards from kit
num_unk = 4  # Number of unknown solutions (variable between 1-12)
num_rep = 1  # Number of repetitions of assay
vol_WR = 200  # Vol in microliters needed per sample
vol_sol = 10  # Vol in microliters of standard or unknown per sample
excess_reagent = 400

metadata = {

    'protocolName': 'BCA Assay (the one)',
    'author': 'DAMP Lab Robotics Colony',
    'description': 'Automatically prepares and performs Pierce Rapid Gold BCA Assay. Load 8 standards into columns 1 and 2 of tube rack in D2. Load Reagent A into Reservoir slot A1, load reagent B into tube rack with standards in slot D6. Put unknown solutions in tube rack in D3. Following experiment completion immediately transfer well plate to microplate reader',
    'source': 'DAMP Lab Robotics Colony'

}

requirements = {
    'robotType': 'Flex',
    'apiLevel': '2.28'
}


def run(protocol: protocol_api.ProtocolContext):
    # Load trash bin
    trash = protocol.load_trash_bin('A3')

    # Load Modules
    thermocycler = protocol.load_module('thermocyclerModuleV2')
    temp_module = protocol.load_module('temperatureModuleV2', 'C3')
    temp_adapter = temp_module.load_adapter('opentrons_aluminum_flat_bottom_plate')

    heater_shaker = protocol.load_module('heaterShakerModuleV1', 'C1')
    heater_shaker_adapter = heater_shaker.load_adapter('opentrons_universal_flat_adapter')
    # Opening heater shaker to put in well plate
    heater_shaker.open_labware_latch()

    # Load labware
    tube_rack_std = protocol.load_labware('opentrons_24_tuberack_nest_1.5ml_snapcap', 'D2')
    tube_rack_unk = protocol.load_labware('opentrons_24_tuberack_nest_1.5ml_snapcap', 'D3')
    reagent_reservoir = protocol.load_labware('usascientific_12_reservoir_22ml', 'D1')
    wellplate = heater_shaker_adapter.load_labware('nunc_96_wellplate_optical_bottom_400ul')

    heater_shaker.close_labware_latch()

    # Load tip racks
    tiprack_1k_1 = protocol.load_labware('opentrons_flex_96_tiprack_1000ul', 'B2')
    tiprack_1k_2 = protocol.load_labware('opentrons_flex_96_tiprack_1000ul', 'B3')
    tiprack_small = protocol.load_labware('opentrons_flex_96_tiprack_200ul', 'A2')

    # Load pipettes
    pip_multi = protocol.load_instrument('flex_8channel_1000', 'left', tip_racks=[tiprack_1k_1])
    pip_single = protocol.load_instrument('flex_1channel_1000', 'right', tip_racks=[tiprack_1k_2, tiprack_small])

    pip_single.default_speed = 750
    pip_single.flow_rate.aspirate = 450
    pip_single.flow_rate.dispense = 450

    pip_multi.default_speed = 750
    pip_multi.flow_rate.aspirate = 450
    pip_multi.flow_rate.dispense = 450

    protocol.comment('All labware/modules loaded')

    # Define reagent positions
    reagent_a_source = reagent_reservoir['A1']
    reagent_b_tube = tube_rack_std['D6']
    wr_source = reagent_reservoir['A2']

    # Calculate amount of working reagent needed for assay and quantities of reagents to use
    expected_WR = (num_std + num_unk) * num_rep * vol_WR + excess_reagent
    reagent_a_ul = expected_WR * (50/51)  # Add excess to ensure enough in reservoir
    reagent_b_ul = reagent_a_ul/50
   

    # Define liquids
    reagent_a = protocol.define_liquid(
        name='Reagent A',
        description='BCA Reagent A',
        display_color='#00FF00'
    )
    reagent_b = protocol.define_liquid(
        name='Reagent B',
        description='BCA Reagent B',
        display_color='#0000FF'
    )
    bsa_standards = protocol.define_liquid(
        name='BSA Standard',
        description='BSA protein standard',
        display_color='#FF0000'
    )
    unknown_samples = protocol.define_liquid(
        name='Unknown Samples',
        description='Unknown protein samples',
        display_color='#FFFF00'
    )

    
         

        
        

    # Compile list of locations to be used (filled by column Ex: A1, B1, C1, ...)
    loc_on_wellplate = [f'{r}{c}' for c in range(1, 13) for r in 'ABCDEFGH'][0:num_std * num_rep + num_unk * num_rep]

    # Define source locations for tube rack
    std_source = [f'{r}{c}' for c in [1, 2] for r in 'ABCD'][:num_std]  # Iterates using two loops to create a list of strings A1, B1, C2, ..., D2
    # Same technique as before to create list, list is then sliced to the correct length
    unk_source = [f'{r}{c}' for c in list(range(1, 7)) for r in 'ABCD'][:num_unk]

    # Full columns of wellplate
    num_std_full = (num_std * num_rep) // 8  # Could just use num_rep, used num_std_full for clarity
    num_unk_full = ((num_unk * num_rep) - ((num_unk * num_rep) % 8)) // 8  # Columns that are fully filled by unknowns
    num_unk_partial = ((num_unk * num_rep) - (num_unk_full * 8))  # Number of unknown samples that do not make a full column
    full_col = num_std_full + num_unk_full  # Total number of full columns

     # Locations of unknowns in partially filled column
    loc_unk_partial = [f'{r}{full_col + 1}' for r in 'ABCDEFGH'[0:num_unk_partial]]


    # Loading Liquids for Visualization
    reagent_a_source.load_liquid(liquid = reagent_a, volume = 10000)
    reagent_b_tube.load_liquid(liquid = reagent_b, volume = 1000)
    for i in std_source:
        tube_rack_std[i].load_liquid(liquid = bsa_standards, volume = 1000)
    for i in unk_source:
        tube_rack_unk[i].load_liquid(liquid = unknown_samples, volume = 1000)

    protocol.comment('Liquids loaded')

    protocol.comment('Populating well plate')
    # Dispense standards
    
    for i in std_source:
        pip_single.pick_up_tip(tiprack_small)
        pip_single.aspirate(vol_sol * num_rep, tube_rack_std[i])
        for j in range(1, num_rep + 1):
            pip_single.dispense(vol_sol, wellplate[loc_on_wellplate[0]])
            pip_single.blow_out(wellplate[loc_on_wellplate[0]])
            loc_on_wellplate = loc_on_wellplate[1:]
        pip_single.drop_tip()

    # Dispense unknowns
    for i in unk_source:
        pip_single.pick_up_tip(tiprack_small)
        pip_single.aspirate(vol_sol * num_rep, tube_rack_unk[i])
        for j in range(1, num_rep + 1):
            pip_single.dispense(vol_sol, wellplate[loc_on_wellplate[0]])
            pip_single.blow_out(wellplate[loc_on_wellplate[0]])
            loc_on_wellplate = loc_on_wellplate[1:]
        pip_single.drop_tip()

    protocol.comment('Creating working reagent')



    # Mixing Working Reagent
    pip_multi.pick_up_tip()
    pip_single.pick_up_tip()


    pip_multi.aspirate(reagent_a_ul / 8, reagent_reservoir['A1'])
    pip_multi.dispense(reagent_a_ul / 8, reagent_reservoir['A2'])
    pip_multi.blow_out(reagent_reservoir['A2'].top(-5))


    # Dispenses volume of reagent b to multiple locations in working reagent reservoir to aid mixing
    res = reagent_reservoir['A2'].bottom(3)
    reservoir_positions = [res.move(Point(y=10 * i)) for i in range(-3, 4)]
    reservoir_positions.reverse()

    pip_single.aspirate(reagent_b_ul, tube_rack_std['D6'])
    for position in reservoir_positions:
        pip_single.dispense(reagent_b_ul / 7, position)
    pip_single.blow_out(reagent_reservoir['A2'].bottom(15))


    pip_multi.flow_rate.aspirate = 150
    pip_multi.flow_rate.dispense = 150

    # Slow speed to decrease bubbles in working reagent while mixing and populating wellplate
    for i in range(2,5,2):
        pip_multi.mix(3, min(expected_WR / 9, 1000), reagent_reservoir['A2'].bottom(i - .7))
    pip_multi.blow_out(reagent_reservoir['A2'].bottom(10))

    

    pip_multi.flow_rate.aspirate = 75
    pip_multi.flow_rate.dispense = 75
    pip_single.flow_rate.aspirate = 75
    pip_single.flow_rate.dispense = 75

   
    protocol.comment('Adding working reagent to well plate')
    #Iterate through full columns and dispense working reagent to 8 wells at a time
    
    
    def low_vol_aspiration(volume, reservoir_model = reagent_reservoir, pipette = pip_single, reservoir_well  = 'A2', new_tip = False):
        """optimized aspiration for reservoir with low volume wells"""

        if new_tip == True:
            pipette.pick_up_tip()

        res_bottoms = reservoir_model[reservoir_well].bottom()
        spacing = reservoir_model[reservoir_well].width / 8
        reservoir_locations = [res_bottoms.move(Point(y = spacing * (i - .5))) for i in range(-3,5)]

        for loc in reservoir_locations[:-1]:
            pipette.aspirate(volume/8, loc)
            pipette.move_to(loc.move(Point(z=7)))   
        pipette.aspirate(volume/8, reservoir_locations[-1])

    num_singles = len(loc_unk_partial)
    max_capacity = 1000 // vol_WR   # At most the pipette can control 1000uL so the most wells it can dispense to per trip is 1000/ the volume per well

    
    for i in range(1, full_col + 1):
        pip_multi.aspirate(vol_WR, wr_source)
        pip_multi.dispense(vol_WR, wellplate[f'A{i}'].top())  #8-tip pipette uses A1-A12 indices instead of A1-H12
        pip_multi.touch_tip(wellplate[f'A{i}'], radius = 0.8, v_offset = -2)

    top_well = wellplate[loc_unk_partial[0]].top(.5) #defining well location at top of the unknown partial column
    loc_unk = [top_well.move(Point(y = -9 * i)) for i in range(num_singles)]  # Convert well locations to points for easier dispensing with single channel pipette

    for i in range(0, num_singles, max_capacity):
        batch = loc_unk[i:i + max_capacity]     # Batch wells into groups of its max capacity
        low_vol_aspiration(vol_WR * len(batch))  # Pick up enough WR to populate batch of wells
        for num, well in enumerate(batch):         # Dispense WR to wells
            pip_single.dispense(vol_WR, well)
            pip_single.touch_tip(wellplate[loc_unk_partial[num]], radius=0.8, v_offset = -2)

    pip_single.drop_tip()
    pip_multi.drop_tip()

    protocol.comment('Starting Incubation')
    heater_shaker.close_labware_latch()
    heater_shaker.set_and_wait_for_shake_speed(1500)
    protocol.delay(seconds=30)
    heater_shaker.deactivate_shaker()

    protocol.comment('Letting rest')
    protocol.delay(minutes=4)
    heater_shaker.open_labware_latch()
    protocol.comment('BCA Protein Assay Complete')
