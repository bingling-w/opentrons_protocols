from opentrons import protocol_api

metadata = {
    'protocolName': 'BSA Serial Dilution in Duplicate',
    'author': 'OpentronsAI',
    'description': 'Serial dilution of BSA stock in duplicate in 1.5mL tubes with three calibrations',
    'source': 'OpentronsAI'
}

requirements = {
    'robotType': 'Flex',
    'apiLevel': '2.25'
}

def run(protocol: protocol_api.ProtocolContext):
    # Load modules
    thermocycler = protocol.load_module('thermocyclerModuleV2')
    heater_shaker = protocol.load_module('heaterShakerModuleV1', 'C1')
    temp_module = protocol.load_module('temperature module gen2', 'C3')
    
    # Load trash bin
    trash = protocol.load_trash_bin('A3')
    
    # Load labware
    tube_rack = protocol.load_labware('opentrons_24_tuberack_nest_1.5ml_snapcap', 'D2')
    water_reservoir = protocol.load_labware('usascientific_12_reservoir_22ml', 'D3')
    
    # Load tip rack
    tiprack = protocol.load_labware('opentrons_flex_96_tiprack_1000ul', 'C2')
    
    # Load pipette
    right_pipette = protocol.load_instrument('flex_1channel_1000', 'right', tip_racks=[tiprack])
    
    # Define wells
    # BSA stock is in D1 (bottom first row)
    bsa_stock = protocol.define_liquid(
        name='BSA stock',
        display_color='#00FF00')
    tube_rack['D1'].load_liquid(liquid=bsa_stock, volume=450)


    water = protocol.define_liquid(
        name='Water stock',
        display_color='#0000FF')
    water_reservoir['A1'].load_liquid(liquid=water, volume=10000)

    
    # Calibration tube 1 positions (A1 and B1)
    cal_tube_1_a = tube_rack['A1']
    cal_tube_1_b = tube_rack['B1']
    
    # Calibration tube 2 positions (A2 and B2)
    cal_tube_2_a = tube_rack['A2']
    cal_tube_2_b = tube_rack['B2']
    
    # Calibration tube 3 positions (A3 and B3)
    cal_tube_3_a = tube_rack['A3']
    cal_tube_3_b = tube_rack['B3']
    
    # Blank positions (A6 and B6)
  #  blank_a = tube_rack['A6']
   # blank_b = tube_rack['B6']
    
    # Step 1: Add water to various tubes using the same tip
    protocol.comment("Step 1: Adding water to tubes")
    
    # Pick up tip once for all water additions
    right_pipette.pick_up_tip()
    
    # Add 200 µL water to calibration tube 1 & 2 (A1, A2, B1, B2)

    right_pipette.aspirate(800, water_reservoir['A1'])
    right_pipette.dispense(200, cal_tube_1_a)
    right_pipette.dispense(200, cal_tube_2_a)
    right_pipette.dispense(200, cal_tube_1_b)
    right_pipette.dispense(200, cal_tube_2_b)
    
    # Add 180 µL water to A3 and B3
    right_pipette.aspirate(360, water_reservoir['A1'])
    right_pipette.dispense(180, cal_tube_3_a)
    right_pipette.dispense(180, cal_tube_3_b)
    
    # Add 1000 µL water to A6 and B6 (blanks)
   # right_pipette.aspirate(1000, water_reservoir['A1'])
   # right_pipette.dispense(1000, blank_a)
   # right_pipette.aspirate(1000, water_reservoir['A1'])
   # right_pipette.dispense(1000, blank_b)
    right_pipette.drop_tip()

    # Step 2: Distribute 200 µL of BSA stock to calibration tube 1 with mix (A1)

    right_pipette.pick_up_tip()
    right_pipette.mix(3, 400, tube_rack['D1'])  # Mix 3 times with 400 µL
    right_pipette.blow_out(tube_rack['D1'].top())
    right_pipette.aspirate(200, tube_rack['D1'])
    right_pipette.dispense(200, cal_tube_1_a)
    right_pipette.mix(3, 200, cal_tube_1_a)  # Mix 3 times with 200 µL
    right_pipette.blow_out(cal_tube_1_a.top())
    right_pipette.drop_tip()

    # Step 2.5: Distribute 200 µL of BSA stock to calibration tube 1 with mix (B1)
    right_pipette.pick_up_tip()
    right_pipette.mix(3, 200, tube_rack['D1'])
    right_pipette.blow_out(tube_rack['D1'].top())
    right_pipette.aspirate(200, tube_rack['D1'])
    right_pipette.dispense(200, cal_tube_1_b)
    right_pipette.mix(3, 200, cal_tube_1_b)  # Mix 3 times with 200 µL
    right_pipette.blow_out(cal_tube_1_b.top())
    right_pipette.drop_tip()

    # Step 3: Performing serial dilution for row A
    protocol.comment("Step 3: Performing serial dilution for row A")

    # Transfer 200 µL from calibration tube 1 (A1) to calibration tube 2 (A2)
    right_pipette.pick_up_tip()
    right_pipette.mix(3, 200, cal_tube_1_a)
    right_pipette.blow_out(cal_tube_1_a.top())
    right_pipette.aspirate(200, cal_tube_1_a)
    right_pipette.dispense(200, cal_tube_2_a)
    right_pipette.mix(3, 200, cal_tube_2_a)  # Mix 3 times with 200 µL
    right_pipette.blow_out(cal_tube_2_a.top())
    right_pipette.drop_tip()
    
    # Transfer 20 µL from calibration tube 2 (A2) to calibration tube 3 (A3)
    right_pipette.pick_up_tip()
    right_pipette.mix(3, 200, cal_tube_2_a)
    right_pipette.blow_out(cal_tube_2_a.top())
    right_pipette.aspirate(20, cal_tube_2_a)
    right_pipette.dispense(20, cal_tube_3_a)
    right_pipette.mix(3, 100, cal_tube_3_a)
    right_pipette.blow_out(cal_tube_3_a.top())
    right_pipette.drop_tip()
    
    # Step 4: Performing serial dilution for row B
    protocol.comment("Step 4: Performing serial dilution for row B")
    
    # Transfer 200 µL from calibration tube 1 (B1) to calibration tube 2 (B2)
    right_pipette.pick_up_tip()
    right_pipette.mix(3, 200, cal_tube_1_b)
    right_pipette.blow_out(cal_tube_1_b.top())
    right_pipette.aspirate(200, cal_tube_1_b)
    right_pipette.dispense(200, cal_tube_2_b)
    right_pipette.mix(3, 200, cal_tube_2_b)
    right_pipette.blow_out(cal_tube_2_b.top())
    right_pipette.drop_tip()

    # Transfer 20 µL from calibration tube 2 (B2) to calibration tube 3 (B3)
    right_pipette.pick_up_tip()
    right_pipette.mix(3, 200, cal_tube_2_b)
    right_pipette.blow_out(cal_tube_2_b.top())
    right_pipette.aspirate(20, cal_tube_2_b)
    right_pipette.dispense(20, cal_tube_3_b)
    right_pipette.mix(3, 100, cal_tube_3_b)
    right_pipette.blow_out(cal_tube_3_b.top())
    right_pipette.drop_tip()

    protocol.pause("Please discard the tip into the clear solid waste container on the bench")
    
    protocol.comment("Serial dilution complete")