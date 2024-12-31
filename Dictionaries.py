petrol_emission_dict = {
                     "Small Car - Petrol":
                         {'emission_value':0.2266},
                     "Medium Car - Petrol":
                         {'emission_value':0.28676},
                     "Large Car - Petrol":
                         {'emission_value':0.43812},
                     "Average Car - Petrol":
                         {'emission_value':0.23679},
                     "Mini - Petrol":
                         {'emission_value':0.209687},
                     "Supermini - Petrol":
                         {'emission_value':0.228027},
                     "Executive - Petrol":
                         {'emission_value':0.341687},
                     "Sports - Petrol":
                         {'emission_value':0.381657},
                     "Dual Purpose 4X4 - Petrol":
                         {'emission_value':0.328387},
                     "MPV - Petrol":
                         {'emission_value':0.296537}
                     }

diesel_emission_dict = {
                     "Small Car - Diesel":
                         {'emission_value':0.2242},
                     "Medium Car - Diesel":
                         {'emission_value':0.26902},
                     "Large Car - Diesel":
                         {'emission_value':0.3357},
                     "Average Car - Diesel":
                         {'emission_value':0.27332},
                     "Mini - Diesel":
                         {'emission_value':0.173416},
                     "Supermini - Diesel":
                         {'emission_value':0.212676},
                     "Executive - Diesel":
                         {'emission_value':0.278586},
                     "Sports - Diesel":
                         {'emission_value':0.272686},
                     "Dual Purpose 4X4 - Diesel":
                         {'emission_value':0.325006},
                     "MPV - Diesel":
                         {'emission_value':0.284216}
                     }

motorbike_emission_dict = {
                    "Small Motorbike":
                    {'emission_value':0.13389},
                    "Medium Motorbike":
                    {'emission_value':0.16266},
                    "Large Motorbike":
                    {'emission_value':0.21326},
                    "Average Motorbike":
                    {'emission_value':0.18294}                     
                    }

#Unlike the above, the below are averages per usage for household appliances
appliances = {
                #contains arbitrary values for testing until accurate data can be sourced
              "oven":{'emission_value':0.001122},#test value
              "energy_saving_bulb":{'emission_value':0.000011},#test value
              "LED_Bulb":{'emission_value':0.0011},#test value
              "room":{'emission_value':0.003},#test value
              "small_fridge":{'emission_value':0.0006},#test value - 24 hours value
              "medium_fridge":{'emission_value':0.0007},#test value - 24 hours value
              "large_fridge":{'emission_value':0.0008},#test value - 24 hours value
              "phone":{'emission_value':0.00005},#test value
              "pc_hour":{'emissions_value':0.0008},#test value
              "tv_hour":{'emissions_value':0.0008},#test value
              "games_console_hour":{'emissions_value':0.0005},#test value
              "washer_hour":{'emission_value':0.001},#test value
              "dryer_hour":{'emissions_value':0.001},#test value
              "kettle_use":{'emissions_value':0.000052},#test value
              "other_uses":{'emissions_value':0.00015285}#test value
              }
              