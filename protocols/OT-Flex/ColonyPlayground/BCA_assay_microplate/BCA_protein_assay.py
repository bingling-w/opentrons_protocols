from opentrons import protocol_api

# Edit the numbers here to suit your needs
standards_number = 8
unknown_number = 4
# Note this code can accept up to 23 unknowns and up to 1 to 2 replicates
# or accpet up to 18 unknowns and 3 replicates
replicates_number = 1  # Supports up to 3 replicates depending on number of unknowns
volume_reagent_per_sample = 200  # uL

metadata = {
    'protocolName': 'BCA Protein Assay Kit',
    'author': 'OpentronsAI',
    'description': 'Automated liquid handling for Pierce BCA Protein Assay to determine protein concentrations',
    'source': 'OpentronsAI'
}

requirements = {
    'robotType': 'Flex',
    'apiLevel': '2.25'
}


def run(protocol: protocol_api.ProtocolContext):
    # Load trash bin
    trash = protocol.load_trash_bin('A3')

    # Load modules
    thermocycler = protocol.load_module('thermocyclerModuleV2')
    temp_module = protocol.load_module('temperature module gen2', 'C3')
    heater_shaker = protocol.load_module('heaterShakerModuleV1', 'C1')

    # Load labware
    reservoir = protocol.load_labware('nest_12_reservoir_15ml', 'C2')
    tube_rack = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 'D1')

    # Load heater shaker adapter
    hs_adapter = heater_shaker.load_adapter("opentrons_universal_flat_adapter")

    # Load labware on heater shaker module
    temp_plate = hs_adapter.load_labware(
        "nunc_96_wellplate_optical_bottom_400ul",
        label="Nunc well plate on Heater_Shaker"
    )

    # Load tip racks for all operations
    tiprackmulti = protocol.load_labware('opentrons_flex_96_tiprack_1000ul', 'B2')
    tipracksingle = protocol.load_labware('opentrons_flex_96_tiprack_1000ul', 'B3')

    # Load pipettes
    p1000_single = protocol.load_instrument(
        'flex_1channel_1000',
        mount='right',
        tip_racks=[tipracksingle]
    )
    p1000_multi = protocol.load_instrument(
        'flex_8channel_1000',
        mount='left',
        tip_racks=[tiprackmulti]
    )

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
    bsa_standard = protocol.define_liquid(
        name='BSA Standard',
        description='BSA protein standard',
        display_color='#FF0000'
    )
    bsa_unknown = protocol.define_liquid(
        name='BSA unknowns',
        description='BSA unknowns made in dilution',
        display_color='#FFFF00'
    )

    # Calculating total reagent needed
    if 0 < unknown_number <= 8:
        channel8_amount = 8
    elif 8 < unknown_number <= 16:
        channel8_amount = 16
    else:
        channel8_amount = 24
    total_reagent = round(((standards_number + channel8_amount) * replicates_number * volume_reagent_per_sample) * 1.20)
    protocol.comment('Total Reagent needed: {total_reagent}')

    # Load liquids into labware
    reservoir['A1'].load_liquid(liquid=reagent_a, volume=15000)
    tube_rack['D6'].load_liquid(liquid=reagent_b, volume=1500)

    # Load BSA standards in column 1 of microplate (8 standards in wells A1-H1)
    for well in temp_plate.columns()[0]:
        well.load_liquid(liquid=bsa_standard, volume=70)

    # Establishing where the unknowns will go in the tube rack
    unknown_sources = tube_rack.wells()[:unknown_number]

    # Load BSA unknowns into the tube
    for well in unknown_sources:
        well.load_liquid(liquid=bsa_unknown, volume=200)

    # Close heater shaker latch
    heater_shaker.close_labware_latch()

    # ===== STEP 1: Microplate Procedure - Transferring Standards =====
    protocol.comment('Transferring BSA standards to columns')

    # Get the replicate destination columns (columns 2, 3, 4, etc.)
    dest_columns = temp_plate.columns()[1:replicates_number + 1]

    protocol.comment(f'Distributing standards to {replicates_number} replicate columns')

    # Distribute from source to all replicate columns
    p1000_multi.pick_up_tip()
    p1000_multi.aspirate(10 * replicates_number, temp_plate.columns()[0][0])

    for dest in dest_columns:
        p1000_multi.dispense(10, dest[0])  # Access first well of each column

    p1000_multi.drop_tip()

    # ===== STEP 2: Microplate Procedure - Transferring Unknowns =====

    protocol.comment('Transferring unknown samples to well plate')

    # Calculate how many columns are needed for unknowns
    import math
    columns_per_replicate = math.ceil(unknown_number / 8)

    # Calculate starting column for unknowns (after standards columns)
    unknown_start_column = replicates_number + 1

    # Transfer unknowns to replicate columns
    for source_idx, source in enumerate(unknown_sources):
        # Collect all destination wells for this source across all replicates
        all_destinations = []

        for replicate in range(replicates_number):
            # Calculate which column and row this unknown goes to
            column_offset = source_idx // 8  # Which column within the replicate (0, 1, 2...)
            row_in_column = source_idx % 8  # Which row within that column (0-7)

            # Calculate the destination column for this replicate
            dest_column = unknown_start_column + (replicate * columns_per_replicate) + column_offset
            destination_well = temp_plate.columns()[dest_column][row_in_column]
            all_destinations.append(destination_well)

        protocol.comment(f'Transferring unknown {source_idx + 1} to {replicates_number} replicates')

        p1000_single.pick_up_tip()
        p1000_single.mix(2, 100, source)  # Mix at source before aspirating
        p1000_single.blow_out(source.top())
        p1000_single.aspirate(10 * replicates_number, source)  # Single source (will be stretched to match destinations)

        for dest in all_destinations:  # List of destinations
            p1000_single.dispense(10, dest)

        p1000_single.drop_tip()

    # ===== STEP 3: Prepare BCA Working Reagent =====
    reagent_a_volume = total_reagent  # µL
    reagent_b_volume = (total_reagent / 50)  # µL
    reagent_mix_volume_8channel = ((total_reagent * 0.40) / 8)

    protocol.comment('Preparing BCA working reagent in reservoir A2')

    # Transfer Reagent A to reservoir A2
    p1000_single.transfer(
        reagent_a_volume,
        reservoir['A1'],
        reservoir['A2'],
        new_tip='once'
    )

    # Transfer Reagent B to reservoir A2
    p1000_single.transfer(
        reagent_b_volume,
        tube_rack['D6'],
        reservoir['A2'],
        new_tip='once'
    )

    # ===== STEP 4: Adding Working Reagent to Standards =====
    protocol.comment('Adding working reagent to standards')

    # Add 200 µL working reagent to each standards replicate column

    p1000_multi.pick_up_tip()
    p1000_multi.mix(3, 100, reservoir['A2'])
    p1000_multi.blow_out(reservoir['A2'].top())
    p1000_multi.aspirate(200, reservoir['A2'])
    p1000_multi.dispense(200, temp_plate['A2'])
    p1000_multi.blow_out(temp_plate['A2'].top())
    p1000_multi.drop_tip()

    if replicates_number > 1:
        dest_columns_WR = temp_plate.columns()[2:replicates_number + 1]
        p1000_multi.transfer(
            200,
            reservoir['A2'],
            dest_columns_WR,
            blow_out=True,
            blowout_location='destination well',
            new_tip='always'
        )

    # ===== STEP 5: Adding Working Reagent to Unknowns =====

    protocol.comment('Adding working reagent to unknowns')

    # Add 200 µL working reagent to each unknowns replicate column
    # The unknowns are already placed in columns starting from unknown_start_column
    # Each replicate occupies one column
    for replicate in range(replicates_number * columns_per_replicate):
        unknown_dest_column = unknown_start_column + replicate
        protocol.comment(f'Adding reagent to unknowns (column {unknown_dest_column + 1})')

        # Add reagent to the column containing unknowns for this replicate
        # The 8-channel pipette will add reagent to all 8 rows (A-H)
        # Even though we only have 9 unknowns (filling A-H in first column, A in potential second)
        # we only need to add to the columns where we placed unknowns
        p1000_multi.transfer(
            200,
            reservoir['A2'],
            temp_plate.columns()[unknown_dest_column][0],
            blow_out=True,
            blowout_location='destination well',
            new_tip='always'
        )

    # ===== STEP 6: Shake =====
    protocol.comment("Shaking at 900 rpm")
    heater_shaker.set_and_wait_for_shake_speed(900)  # Set to 900 rpm and wait
    protocol.delay(seconds=20)  # Shake for 20 seconds

    # Stop shaking
    heater_shaker.deactivate_shaker()

    # Open heater shaker latch
    heater_shaker.open_labware_latch()

    protocol.comment('Incubating at room temperature for 4 minutes and 10 seconds')
    protocol.delay(seconds=250)

    protocol.comment('BCA Protein Assay protocol complete, please send wellplate to platereader immediately, 480nm')

