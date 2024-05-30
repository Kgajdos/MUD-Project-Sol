TECH_TREE = {
    #Medical Tech
    "basic_medbay_tech": {
    "name": "Basic Medical Bay",
    "research": 1000,
    "requires": [None],
},

    "advanced_medbay_tech": {
        "name": "Advanced Medical Bay",
        "research": 5000,
        "requires": ["basic_medbay_tech"],
    },
    "trauma_center": {
        "name": "Trauma Center",
        "research": 25000,
        "requires": ["advanced_medbay_tech"],
    },

    #Dining Tech
    "basic_defac": {
        "name": "Basic Dining Facility",
        "research": 1000,
        "requires": [None],
    },
    "advanced_defac": {
        "name": "Advanced Dining Facility",
        "research": 5000,
        "requires": ["basic_defac"],
    },
    "canteen": {
        "name": "Canteen",
        "research": 25000,
        "requires": ["advanced_defac"],
    },

    #Quarters Tech
    "basic_living_quarters": {
        "name": "Basic Living Quarters",
        "research": 1000,
        "requires": [None],
    },
    "advanced_living_quarters": {
        "name": "Advanced Living Quarters",
        "research": 5000,
        "requires": ["basic_living_quarters"],
    },
    "apartments": {
        "name": "Apartments",
        "research": 25000,
        "requires": ["advaneced_living_quarters"],
    },

    #Food Production tech
    "basic_hydroponics": {
        "name": "Basic Hydroponics Grow Room",
        "research": 1000,
        "requires": [None],
    },
    "advanced_hydroponics": {
        "name": "Advanced Hydroponics Grow Room",
        "research": 5000,
        "requires": ["basic_hydroponics"],
    },
    "greenhouse": {
        "name": "Greenhouse",
        "research": 25000,
        "requires": ["advanced_hydroponics"],
    },

    #Metallurgy tech
    "basic_foundary": {
        "name": "Basic Foundary",
        "research": 1000,
        "requires": [None],
    },
    "advanced_foundary": {
        "name": "Advanced Foundary",
        "research": 5000,
        "requires": ["basic_foundary"],
    },
    "forge": {
        "name": "Forge",
        "research": 25000,
        "requires": ["advanced_foundary"],
    },

    #Item Creation Tech
    "basic_fabricator": {
        "name": "Basic Fabricator",
        "research": 1000,
        "requires": [None],
    },
    "advanced_fabricator": {
        "name": "Advanced Fabricator",
        "research": 5000,
        "requires": ["basic_fabricator"],
    },
    "factory": {
        "name": "Factory",
        "research": 25000,
        "requires": ["advanced_fabricator"],
    },

    #Station Tech
    "basic_outpost": {
        "name": "Basic Outpost",
        "research": 10000,
        "requires": ["basic_medbay_tech", "basic_defac", "basic_living_quarters", ]
    },

    #Space Station
    "space_station": {
        "name": "Space Station",
        "research": 15000,
        "requires": ["trauma_center", "canteen", "greenhouse", "forge", "factory"]
    },

    #SpaceTime Barge
    "spacetime_barge": {
        "name": "SpaceTime Barge",
        "research": 20000,
        "requires": ["space_station"]
    }
}