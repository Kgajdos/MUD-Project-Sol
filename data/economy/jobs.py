from items.items import ITEM_DEFINITIONS

JOBS = {
    #METAL WORKING
    "make_steel_plate": {
        "item_key": "steel_plate",
        "materials": {"iron": 3, "carbon": 1},
        "production_time": 30,   # time per unit
        "required_research": None,
        "category": "smelting"
    },
    "make_aluminum_sheet": {

    },
    "make_titanium_panel": {

    },
    "make_copper_wiring": {

    },
    "make_gold_plating": {

    },
    "make_platinum_alloy": {

    },
    "make_silver_conductor": {

    },
    "make_iron_bar": {

    },
    "make_nickel_coil": {

    },
    "make_silicate_glass": {

    },
    "make_carbon_rod": {

    },
    "make_palladium_coating": {

    },
    "make_bearing_joint": {

    },
    "make_gear_casing": {

    },
    "make_compression_spring": {

    },
    #ELECTRONICTS & ENERGY
    "make_circuit_board": {
        "item_key": "circuit_board",
        "materials": {"copper": 2, "silicate": 1, "gold": 1},
        "production_time": 60,
        "required_research": "basic_electronics",
        "category": "electronics"
    },
    "make_energy_cell": {
        "item_key": "energy_cell",
        "materials": {"platinum": 1, "silicate": 2, "hydrogen": 2},
        "production_time": 45,
        "required_research": "basic_energy_storage",
        "category": "power"
    },
    "make_optical_fiber": {

    },
    "make_microchip": {

    },
    "make_thermal_sensor": {

    },
    "make_control_module": {

    },
    "make_logic_array_gate": {

    },
    "make_digital_interface": {

    },
    "make_signal_amplifier": {

    },
    "make_wireless_node": {

    },
    "make_power_regulator": {

    },
    "make_hardlight_emitter": {

    },
    "make_nano_insulator": {

    },
    #SHIP COMPONENTS & PARTS
    "make_thruster_nozzle": {

    },
    "make_nav_array": {

    },
    "make_life_support_unit": {

    },
    "make_fuel_tank": {

    },
    "make_shield_generator": {

    },
    "make_armor_plating": {
        
    },
    "make_sensor_array": {

    },
    "make_gyro_stabilizer": {

    },
    "make_grav_plate": {

    },
    "make_fusion_core": {

    },
    "make_hull_patch_kit": {

    },
    "make_engine_mount": {

    },
    "make_solar_collector": {

    },
    "make_reactor_core_casing": {

    },
    "make_airlock_mechanism": {

    },
    "make_comms_array": {

    },
    #TOOLS & FIELD GEAR
    "make_repair_kit": {

    },
    "make_mining_laser": {

    },
    "make_diagnostic_scanner": {

    },
    "make_decontamination_spray": {

    },
    "make_plasma_cutter": {

    },
    "make_oxygen_filter": {

    },
    "make_radiation_shield_pad": {

    },
    "make_welding_goggles": {

    },
    "make_power_gloves": {

    },
    "make_tether_line": {

    },
    "make_fabricator_hand_tool": {

    },
    "make_modular_toolset": {

    },
    #SCIENCE/RESEARCH EQUIPMENT
    "make_research_probe": {

    },
    "make_data_recorder": {

    },
    "make_scanning_satellite": {

    },
    "make_enviroment_sampler": {

    },
    "make_gene_sequencer": {

    },
    "make_autoclave_unit": {

    },
    "make_nanite_harvester": {

    },
    "make_lab_vial_pack": {

    },
    "make_radiation_counter": {

    },
    "make_ai_uplink_node": {

    },
    "make_bio_reactor_core": {

    },
    "make_field_study_kit": {

    },
    "make_neural_adapter": {

    },
    #MEDICAL & SURVIVAL GOODS
    
}