from opentrons import protocol_api

# Edit the numbers here to suit your needs
bacteria_number = 8 # up to 96 (keep to multiples of 8 for the multichannel pipette)

metadata = {
    'protocolName': 'Promega Miniprep Draft',
    'author': 'Bing',
    'description': 'Automated miniprep protocol using the promega magnesil kit'
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
    binding_plate = protocol.load_labware('greiner_96_microplate_280ul', 'A2')

    reservoir = temp_module.load_labware('usascientific_12_reservoir_22ml')

    # Load heater shaker adapter
    hs_adapter = heater_shaker.load_adapter("opentrons_universal_flat_adapter")
    # Load labware on heater shaker adapter
    deep_wellplate = hs_adapter.load_labware(
        "greiner_96_wellplate_2000ul",
        label="Deep wellplate on heater"
    )

    #Load magnetic block
    mag_block = protocol.load_module("magneticBlockV1", "D1") 
    # Load a compatible 96‑well plate onto the magnetic block
    clearing_plate = mag_block.load_labware("greiner_96_microplate_280ul") 

    # Load tip racks for all operations
    tiprack1000 = protocol.load_labware('opentrons_flex_96_tiprack_1000ul', 'B2')
    tiprack200 = protocol.load_labware('opentrons_flex_96_tiprack_200ul', 'B3')

    # Load pipettes
    p1000_multi = protocol.load_instrument(
        'flex_8channel_1000',
        mount='right',
        tip_racks=[tiprack1000, tiprack200]
    )

    # Define liquids
    bacterial_culture = protocol.define_liquid(
        name='Bacterial culture',
        display_color="#000000"
    )
    resuspension_solution = protocol.define_liquid(
        name='Resuspension Solution',
        display_color='#00FF00'
    )
    lysis_solution = protocol.define_liquid(
        name='Cell lysis solution',
        display_color="#73D3BB"
    )
    neutralization_solution = protocol.define_liquid(
        name='neutralization_solution',
        display_color='#FFFF00'
    )
    magnesil_blue = protocol.define_liquid(
        name='Magnesil Blue',
        display_color="#3A93E6"
    )
    magnesil_red = protocol.define_liquid(
        name='Magnesil Red',
        display_color="#CC2121"
    )

    elution_buffer = protocol.define_liquid(
        name='Elution Buffer',
        display_color="#913FFC"
    )

    ethanol_80 = protocol.define_liquid(
        name='80 percent Ethanol',
        display_color="#D6D6D6"
    )

    # Load liquids into labware
    reservoir['A1'].load_liquid(liquid=resuspension_solution, volume=1000)
    reservoir['A2'].load_liquid(liquid=lysis_solution, volume=1000)
    reservoir['A3'].load_liquid(liquid=neutralization_solution, volume=1000)
    reservoir['A4'].load_liquid(liquid=magnesil_blue, volume=1000)
    reservoir['A5'].load_liquid(liquid=magnesil_red, volume=1000)
    reservoir['A6'].load_liquid(liquid=ethanol_80, volume=5000)
    reservoir['A7'].load_liquid(liquid=elution_buffer, volume=1000)

    # Establishing where the bacteria culture will go in the deep well plate
    bacteria_location = deep_wellplate.wells()[:bacteria_number]
    # Load bacterial culture into the deep well plate
    for well in bacteria_location:
        well.load_liquid(liquid=bacterial_culture, volume=1000)

    # ========================= STEP 1: Cell Resuspension =======================================================
    protocol.comment('Adding 90 uL of resuspension solution to the deep well plate')

    # Close heater shaker latch
    heater_shaker.close_labware_latch()

    # Determining where the 8-channel pipette will go
    well_location = []
    for i in range(int(bacteria_number / 8)):
        well_location.append(8 * i)
    
    deep_well_dest_top = [deep_wellplate.wells()[well].top(-2) for well in well_location]
  
    p1000_multi.distribute(
        90,
        reservoir['A1'],
        deep_well_dest_top,
        touch_tip=True,
        new_tip='once',
        )
    
    #heater_shaker.set_and_wait_for_shake_speed(1350)  # Set rpm
    #protocol.delay(minutes=5)  # Shake for 5 minutes

    # Stop shaking
    #heater_shaker.deactivate_shaker()

    # ========================= STEP 2: Cell Lysis and Lysate Clearing =======================================================
    protocol.comment('Adding 120 uL of lysis solution to the deep well plate')
    
    p1000_multi.distribute(
        120,
        reservoir['A2'],
        deep_well_dest_top,
        touch_tip=True,
        new_tip='once',
        disposal_volume=0
        )

    #heater_shaker.set_and_wait_for_shake_speed(810)  # Set rpm
    #protocol.delay(minutes=3)  # Shake for 3 minutes

    # Stop shaking
    #heater_shaker.deactivate_shaker()

    protocol.comment('Adding 120 uL of neutralization solution to the deep well plate')
    
    p1000_multi.distribute(
        120,
        reservoir['A3'],
        deep_well_dest_top,
        touch_tip=True,
        new_tip='once',
        disposal_volume=0
        )

    #heater_shaker.set_and_wait_for_shake_speed(1350)  # Set rpm
    #protocol.delay(minutes=3)  # Shake for 3 minutes

    # Stop shaking
    #heater_shaker.deactivate_shaker()

    protocol.comment('Adding 25 uL of magnesil blue to the deep well plate')
    
    p1000_multi.pick_up_tip(tiprack200)
    p1000_multi.distribute(
        25,
        reservoir['A4'],
        deep_well_dest_top,
        touch_tip=True,
        new_tip='never',
        disposal_volume=0
        )
    p1000_multi.drop_tip()

    #heater_shaker.set_and_wait_for_shake_speed(1350)  # Set rpm
    #protocol.delay(minutes=1)  # Shake for 1 minute

    # Stop shaking
    #heater_shaker.deactivate_shaker()

    protocol.comment('Adding 300 uL of neutralized lysis from the deep well plate to the clearing plate')

    clearing_plate_dest = [clearing_plate.wells()[well] for well in well_location]
    deep_well_dest_middle = [deep_wellplate.wells()[well] for well in well_location]

    for src, dest in zip(deep_well_dest_middle, clearing_plate_dest):
       p1000_multi.transfer(
           300,
           src,
           dest,
           touch_tip=True,
           new_tip='always'
        )
    
    protocol.comment('Delaying for 90 seconds to allow the magnetized pellet to form')

    #protocol.delay(seconds=90)  # delay 90 seconds


    # ========================= STEP 3: DNA Binding =======================================================

    protocol.comment('Adding 25 uL of magnesil red to the new binding plate')

    protocol.move_labware(
        labware=binding_plate,
        new_location="D2", 
        use_gripper=True,  
        pick_up_offset={"x": 0, 'y': 0, 'z': (13*2)},    # Fine-tune if needed
        drop_offset={"x": 0, 'y': 0, 'z': 2.5}        # Fine-tune stacking height
    )

    #Determining where the 8-channel pipette will go in the binding plate
    binding_plate_dest_top = [binding_plate.wells()[well].top(-0.2) for well in well_location]

    p1000_multi.pick_up_tip(tiprack200)
    p1000_multi.distribute(
        25,
        reservoir['A5'],
        binding_plate_dest_top,
        touch_tip=True,
        new_tip='never',
        disposal_volume=0
        )
    p1000_multi.drop_tip()
    
    protocol.comment('Adding 120 uL of the clear lysate to the new binding plate')

    for src, dest in zip(clearing_plate_dest, binding_plate_dest_top):
       p1000_multi.pick_up_tip(tiprack200)
       p1000_multi.transfer(
           120,
           src,
           dest,
           touch_tip=True,
           new_tip='never'
        )
       p1000_multi.drop_tip()
       
    # Open heater shaker latch
    heater_shaker.open_labware_latch()
    
    protocol.move_labware(deep_wellplate, new_location="C2", use_gripper=True) 

    protocol.move_labware(
        binding_plate,
        new_location=hs_adapter,
        use_gripper=True,
        pick_up_offset={"x": 0, 'y': 0, 'z': -2},    # Fine-tune if needed
        drop_offset={"x": 0.5, 'y': 0, 'z': -3}
    ) 

    heater_shaker.close_labware_latch()

    #heater_shaker.set_and_wait_for_shake_speed(1200)  # Set rpm
    #protocol.delay(minutes=2)  # Shake for 2 minutes

    # Stop shaking
    #heater_shaker.deactivate_shaker()
    heater_shaker.open_labware_latch()

    protocol.move_labware(
        clearing_plate,
        new_location="D3",
        use_gripper=True,
        pick_up_offset={"x": 0, 'y': 0, 'z': -2},    # Fine-tune if needed
        drop_offset={"x": 0, 'y': 0, 'z': 0}
    ) 

    protocol.move_labware(
        binding_plate,
        new_location=mag_block,
        use_gripper=True,
        drop_offset={"x": 0, 'y': 0, 'z': -4.5} #perfect offset
    )

    protocol.comment('Removing supernatant from the binding plate')

    binding_plate_supernatant_removal = [binding_plate.wells()[well].bottom(2) for well in well_location]

    p1000_multi.transfer(
        110,
        binding_plate_supernatant_removal,
        reservoir['A12'],
        new_tip = 'always',
        tip_rack = [tiprack200]
    )

    protocol.move_labware(
        binding_plate,
        new_location=hs_adapter,
        use_gripper=True,
        pick_up_offset={"x": 0, 'y': 0, 'z': -2},
        drop_offset={"x": 0.5, 'y': 0, 'z': 2}
    )

    heater_shaker.close_labware_latch()

    protocol.move_labware(
        clearing_plate,
        new_location=mag_block,
        use_gripper=True,
        pick_up_offset={"x": 0, 'y': 0, 'z': -2},
        drop_offset={"x": 0.5, 'y': 0, 'z': -5.7}
    )

    protocol.comment('Adding 25 uL more Magnesil Red to the binding plate')

    binding_plate_dest_top = [binding_plate.wells()[well].top(-0.2) for well in well_location]

    p1000_multi.distribute(
        25,
        reservoir['A5'],
        binding_plate_dest_top,
        touch_tip=True,
        new_tip='once',
        disposal_volume=0,
        tip_rack = [tiprack200]
    )

    protocol.comment('Adding reamaining 120 uL of the clear lysate to the binding plate')

    p1000_multi.transfer(
        120,
        clearing_plate_dest,
        binding_plate_dest_top,
        touch_tip=True,
        new_tip='once',
        tip_rack= [tiprack200]
    )
    
    #heater_shaker.set_and_wait_for_shake_speed(1200)  # Set rpm
    #protocol.delay(minutes=2)  # Shake for 2 minutes
    heater_shaker.open_labware_latch()

    protocol.comment('Moving clearing plate offdeck')
    protocol.move_labware(
        clearing_plate,
        new_location="D3",
        use_gripper=True,
        drop_offset={"x": 175, 'y': 0, 'z': 10} 
    )

    del protocol.deck["D3"]

    protocol.move_labware(
        binding_plate,
        new_location=mag_block,
        use_gripper=True,
        drop_offset={"x": 0, 'y': 0, 'z': -5} #perfect offset
    )

    protocol.comment('Removing supernatant from the binding plate')

    p1000_multi.transfer(
        110,
        binding_plate_supernatant_removal,
        reservoir['A12'],
        tip_rack = 'tiprack200'
    )
    
    # ========================= STEP 4: Washing =======================================================
    
    protocol.comment('Washing Binding plate 3 times')

    binding_plate_dest_top = [binding_plate.wells()[well].top(-0.2) for well in well_location]

    for i in range(2):
        p1000_multi.pick_up_tip(tiprack200)

        p1000_multi.transfer(
            100,
            reservoir['A6'],
            binding_plate_dest_top,
            touch_tip=True,
            new_tip='never',
        )

        heater_shaker.open_labware_latch()

        protocol.move_labware(
            binding_plate,
            new_location=hs_adapter,
            use_gripper=True,
            pick_up_offset={"x": 0, 'y': 0, 'z': -2},
            drop_offset={"x": 0.5, 'y': 0, 'z': 3}
        )

        heater_shaker.close_labware_latch()
        #heater_shaker.set_and_wait_for_shake_speed(1200)  # Set rpm
        #protocol.delay(minutes=1)  # Shake for 2 minute
        heater_shaker.open_labware_latch()

        protocol.move_labware(
            binding_plate,
            new_location=mag_block,
            use_gripper=True,
            pick_up_offset={"x": 0, 'y': 0, 'z': -2}
            drop_offset={"x": 0, 'y': 0, 'z': -4.5} #perfect offset
        )

        #protocol.delay(minutes=2)  # Allow pellet to form for 2 minute

        protocol.comment('Removing spent wash from the binding plate')

        binding_plate_supernatant_removal = [binding_plate.wells()[well].bottom(2) for well in well_location]

        p1000_multi.transfer(
            100,
            binding_plate_supernatant_removal,
            reservoir['A11'],
            new_tip='never'
        )
        p1000_multi.drop_tip()

    # ========================= STEP 5: Drying =======================================================

    protocol.comment('Drying binding plate for 10 minutes')
    #protocol.delay(minutes=10)

    protocol.move_labware(
        binding_plate,
        new_location=hs_adapter,
        use_gripper=True,
        pick_up_offset={"x": 0, 'y': 0, 'z': -2},
        drop_offset={"x": 0.5, 'y': 0, 'z': 3}
    )

    # ========================= STEP 6: Elution of DNA =======================================================
    
    protocol.comment('Adding 100 uL of elution buffer into the binding plate')  

    heater_shaker.close_labware_latch()

    binding_plate_dest_top = [binding_plate.wells()[well].top(-0.2) for well in well_location]
    p1000_multi.transfer(
        100,
        reservoir['A7'],
        binding_plate_dest_top,
        touch_tip=True,
        new_tip='once'
    ) 

    #heater_shaker.set_and_wait_for_shake_speed(1200)  # Set rpm
    #protocol.delay(minutes=2)  # Shake for 2 minute
    heater_shaker.open_labware_latch()

    protocol.move_labware(
        binding_plate,
        new_location=mag_block,
        use_gripper=True,
        drop_offset={"x": 0, 'y': 0, 'z': -5} #perfect offset
    )

    protocol.comment('Moving elution plate')  
    elution_plate = protocol.load_labware('greiner_96_microplate_280ul', 'A2')

    protocol.move_labware(
        labware=elution_plate,
        new_location="D2", 
        use_gripper=True,  
        pick_up_offset={"x": 0, 'y': 0, 'z': 13},    # Fine-tune if needed
        drop_offset={"x": 0, 'y': 0, 'z': 2.5}        # Fine-tune stacking height
    )

    protocol.comment('Transferring 80-90 uL of eluate from binding plate to the elution plate')  

    elution_plate_middle = [elution_plate.wells()[well] for well in well_location]
    binding_plate_supernatant_removal = [binding_plate.wells()[well].bottom(2) for well in well_location]

    p1000_multi.transfer(
        90,
        binding_plate_supernatant_removal,
        elution_plate_middle,
        touch_tip=True,
        new_tip='once'
    ) 

    protocol.move_labware(
        binding_plate,
        new_location=hs_adapter,
        use_gripper=True,
        pick_up_offset={"x": 0, 'y': 0, 'z': -2},    # Fine-tune if needed
        drop_offset={"x": 0, 'y': 0, 'z': -3}
    ) 

    heater_shaker.close_labware_latch()

    protocol.move_labware(
        elution_plate,
        new_location=mag_block,
        use_gripper=True,
        drop_offset={"x": 0, 'y': 0, 'z': -2} #perfect offset
    )

    #protocol.delay(minutes=5)  # Stand for 5 minutes

    final_plate = protocol.load_labware('greiner_96_microplate_280ul', 'A2')

    protocol.move_labware(
        labware=final_plate,
        new_location="D2", 
        use_gripper=True,  
        pick_up_offset={"x": 0, 'y': 0, 'z': -1.2},    # Fine-tune if needed
        drop_offset={"x": 0, 'y': 0, 'z': 2.5}        # Fine-tune stacking height
    )

    protocol.comment('Transferring 80-90 uL of eluate from elution plate to the final plate')   

    elution_plate_removal = [elution_plate.wells()[well].bottom(2) for well in well_location]
    final_plate = [final_plate.wells()[well] for well in well_location]
    
    p1000_multi.transfer(
        90,
        elution_plate_removal,
        final_plate,
        touch_tip=True,
        new_tip='once'
    ) 

    heater_shaker.open_labware_latch()

    protocol.comment('Protocol Done')   