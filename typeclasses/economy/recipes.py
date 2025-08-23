GOOD_PROCESSING_RECIPES = {
    ###########################################################
    ######################Iron Products########################
    ###########################################################
    "iron": [{
        "station": "forge",
        "output": "Iron Bar",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "Iron Bar",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs":[
                ("stage", "processed"),
                ("value", 15),
                ("tags", ["metal", "bar"])
            ]      
                    }
    }, {
        "station": "refinery",
        "output": "Iron Powder",
        "input_qty": 1,
        "output_qty": 3,
        "prototype": {
            "key": "Iron Powder",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 8),
                ("tags", ["metal", "powder"])
            ]
        }
    }, {
        "station": "forge",
        "output": "Steel Bar",
        "input_qty": 1,
        "output_qty": 1,
        "other_mats": {
            "carbon": 1
            },
        "prototype": {
            "key": "Steel Bar",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 25),
                ("tags", ["metal", "bar", "alloy"])
            ]
        }
    }
    ],
    ###########################################################
    ####################Copper Products########################
    ###########################################################
    "copper": [{
        "station": "forge",
        "output": "Copper Wire",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "Copper Wire",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 15),
                ("tags", ["metal", "wire"])
            ]
        }
    },{
        "station": "forge",
        "output": "Copper Sheet",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "Copper Sheet",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 15),
                ("tags", ["metal", "sheet"])
            ]
        }
    },{
        "station": "forge",
        "output": "Copper Coil",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "Copper Coil",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 15),
                ("tags", ["metal", "coil"])
            ]
        }
    }
    ],
    ###########################################################
    ####################Nickel Products########################
    ###########################################################
    "nickel":[ {
        "station": "forge",
        "output": "Nickel Rod",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "Nickel Rod",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 15),
                ("tags", ["metal", "rod"])
            ]
        }
    },{
        "station": "forge",
        "output": "Nickel Plate",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "Nickel Plate",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 15),
                ("tags", ["metal", "plate"])
            ]
        }
    },{
        "station": "forge",
        "output": "Invar Alloy",
        "input_qty": 1,
        "output_qty": 1,
        "other_mats": {
            "iron": 1
        },
        "prototype": {
            "key": "Invar Alloy",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 15),
                ("tags", ["metal", "alloy"])
            ]
        }
    }],
    ###########################################################
    ##################Aluminum Products########################
    ###########################################################
    "aluminum": [{
        "station": "forge",
        "output": "Aluminum Bar",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "Aluminum Bar",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 15),
                ("tags", ["metal", "bar"])
            ]
        }
    },{
        "station": "refinery",
        "output": "Aluminum Foil",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "Aluminum Foil",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 15),
                ("tags", ["metal", "foil"])
            ]
        }
    },{
        "station": "forge",
        "output": "Aluminum Sheet",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "Aluminum Sheet",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 15),
                ("tags", ["metal", "sheet"])
            ]
        } 
    }],
    ###########################################################
    ####################Titanium Products######################
    ###########################################################
    "titanium": [{
        "station": "forge",
        "output": "Titanium Bar",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "Titanium Bar",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 15),
                ("tags", ["metal", "bar"])
            ]
        }
    },{
        "station": "refinery",
        "output": "Titanium Mesh",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "Titanium Mesh",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 15),
                ("tags", ["metal", "mesh"])
            ]
        }
    },{
        "station": "forge",
        "output": "Titanium Alloy",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "Titanium Alloy",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 15),
                ("tags", ["metal", "alloy"])
            ]
        }
    }],
    ###########################################################
    ####################Silver Products########################
    ###########################################################
    "silver": [{
        "station": "forge",
        "output": "Silver Bar",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "Silver Bar",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 25),
                ("tags", ["metal", "bar"])
            ]
        }
    },{
        "station": "forge",
        "output": "Silver Wire",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "Silver Wire",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 15),
                ("tags", ["metal", "wire", "luxury"])
            ]
        }
    },{
        "station": "refinery",
        "output": "Silver Dust",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "Silver Dust",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 15),
                ("tags", ["metal", "dust", "medical"])
            ]
        }
    }],
    ###########################################################
    ######################Clay Products########################
    ###########################################################
    "clay": [{
        "station": "refinery",
        "output": "Ceramic Brick",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "Ceramic Brick",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 15),
                ("tags", ["ceramic", "brick"])
            ]
        }
    },{
        "station": "refinery",
        "output": "Porcelain Plate",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "Porcelain Plate",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 15),
                ("tags", ["procelain", "plate"])
            ]
        }
    },{
        "station": "refinery",
        "output": "Terracotta",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "Terracotta",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 15),
                ("tags", ["earthenware"])
            ]
        }
    }],
    ###########################################################
    #################Palladium Products########################
    ###########################################################
    "palladium": [{
        "station": "forge",
        "output": "Palladium Coil",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "Palladium Coil",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 15),
                ("tags", ["metal", "coil"])
            ]
        }
    },{
        "station": "forge",
        "output": "Palladium Plate",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "Palladium Plate",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 15),
                ("tags", ["metal", "plate"])
            ]
        }
    }],
    ###########################################################
    ####################Uranium Products#######################
    ###########################################################
    "uranium": [{
        "station": "forge",
        "output": "Uranium Rod",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "Uranium Rod",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 25),
                ("tags", ["radioactive", "rod"])
            ]
        }
    },{
        "station": "refinery",
        "output": "Depleted Uranium",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "Depleted Uranium",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 25),
                ("tags", ["radioactive", "munitions"])
            ]
        }
    },{
        "station": "fabricator",
        "output": "Fuel Cell",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "Fuel Cell",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 25),
                ("tags", ["radioactive", "fuel"])
            ]
        }
    }],
    ###########################################################
    ####################Quartz Products########################
    ###########################################################
    "quartz": [
        {
        "station": "refinery",
        "output": "Refined Quartz",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "Refined Quartz",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 25),
                ("tags", ["silica"])
            ]
        }
    }, {
        "station": "fabricator",
        "output": "Silicon Wafer",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "Silicon Wafer",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 25),
                ("tags", ["chips", "circuts"])
            ]
        }
    }, {
        "station": "fabricator",
        "output": "Optical Lens",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "Optical Lens",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 25),
                ("tags", ["glass", "gear"])
            ]
        }
    }
    ],
    ###########################################################
    ####################Diamond Products#######################
    ###########################################################
    "diamond": [
        {
        "station": "refinery",
        "output": "Industrial Diamond",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "Industrial Diamond",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 25),
                ("tags", ["gem", "industry"])
            ]
        }
    }, {
        "station": "fabricator",
        "output": "Cut Diamond",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "Cut Diamond",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 25),
                ("tags", ["gem", "industry"])
            ]
        }
    }, {
        "station": "refinery",
        "output": "Diamond Dust",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "Diamond Dust",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 25),
                ("tags", ["gem", "dust"])
            ]
        }
    }
    ],
    ###########################################################
    ####################Emerald Products#######################
    ###########################################################
    "emerald": [
        {
        "station": "fabricator",
        "output": "Cut Emerald",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "Cut Emerald",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 25),
                ("tags", ["gem", "cut"])
            ]
        }
    }, {
        "station": "refinery",
        "output": "Emerald Dust",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "Emerald Dust",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 25),
                ("tags", ["gem", "dust"])
            ]
        }
    }, {
        "station": "fabricator",
        "output": "Jewel Component",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "Jewel Component",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 25),
                ("tags", ["gem", "jewelry"])
            ]
        }
    }
    ],
    ###########################################################
    ####################Ruby Products##########################
    ###########################################################
    "ruby": [
        {
        "station": "fabricator",
        "output": "Ruby Lens",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "Ruby Lens",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 25),
                ("tags", ["gem", "gear"])
            ]
        }
    }, {
        "station": "fabricator",
        "output": "Cut Ruby",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "Cut Ruby",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 25),
                ("tags", ["gem", "jewelry"])
            ]
        }
    }, {
        "station": "fabricator",
        "output": "Synthetic Ruby Chip",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "Synthetic Ruby Chip",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 25),
                ("tags", ["tech", "gear"])
            ]
        }
    }
    ],
    ###########################################################
    ####################Sapphire Products######################
    ###########################################################
    "sapphire": [
        {
        "station": "fabricator",
        "output": "Sapphire Lens",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "Sapphire Lens",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 25),
                ("tags", ["tech", "gear"])
            ]
        }
    }, {
        "station": "fabricator",
        "output": "Cut Sapphire",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "Cut Sapphire",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 25),
                ("tags", ["gem", "jewelry"])
            ]
        }
    }, {
        "station": "fabricator",
        "output": "Watch Glass",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "Watch Glass",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 25),
                ("tags", ["luxury", "gear"])
            ]
        }
    }
    ],
    ###########################################################
    ####################Gold Products##########################
    ###########################################################
    "gold": [
        {
        "station": "forge",
        "output": "Gold Bar",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "Gold Bar",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 25),
                ("tags", ["luxury"])
            ]
        }
    }, {
        "station": "forge",
        "output": "Gold Wire",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "Gold Wire",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 25),
                ("tags", ["metal", "wire"])
            ]
        }
    }, {
        "station": "refinery",
        "output": "Gold Flakes",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "Gold Flakes",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 25),
                ("tags", ["metal", "circuitry"])
            ]
        }
    }
    ],
    ###########################################################
    ####################Platinum Products######################
    ###########################################################
    "platinum": [
        {
        "station": "forge",
        "output": "Platinum Coil",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "Platinum Coil",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 25),
                ("tags", ["metal", "coil"])
            ]
        }
    }, {
        "station": "fabricator",
        "output": "Catalyst Plate",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "catalyst Plate",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 25),
                ("tags", ["metal", "circuitry"])
            ]
        }
    }, {
        "station": "refinery",
        "output": "Platinum Dust",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "Platinum Dust",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 25),
                ("tags", ["metal", "dust"])
            ]
        }
    }
    ],
    ###########################################################
    ####################Silicate Products######################
    ###########################################################
    "silicate": [
        {
        "station": "refinery",
        "output": "Refined Silicon",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "Refined Silicon",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 25),
                ("tags", ["mineral", "silicon"])
            ]
        }
    }, {
        "station": "refinery",
        "output": "Silicone Paste",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "Silicone Paste",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 25),
                ("tags", ["polymer", "synthetic"])
            ]
        }
    }, {
        "station": "refinery",
        "output": "Glass Sheet",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "Glass Sheet",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 25),
                ("tags", ["glass", "sheet"])
            ]
        }
    }, {
        "station": "refinery",
        "output": "Silicon Chip",
        "input_qty": 1,
        "output_qty": 1,
        "prototype": {
            "key": "Silicon Chip",
            "typeclass": "typeclasses.economy.goods.Good",
            "attrs": [
                ("stage", "processed"),
                ("value", 25),
                ("tags", ["component", "tech"])
            ]
        }
    }
    ]
}