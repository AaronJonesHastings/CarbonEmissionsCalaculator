"""The below is taken from the UK government and provides an emission 
value in g of CO2. These are not emission factors """

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

#Unlike the above, the below are averages per usage/hour for household appliances
appliances = {
              #referenced from https://www.carbonfootprint.com/energyconsumption.html
              "gas_oven":{'emission_value':0.28127313101}, #per use
              "electric_oven":{'emission_value':0.67357512953}, #per use
              "energy_saving_bulb":{'emission_value':0.00753424657},
              "standard_bulb":{'emission_value':0.04315068493}, #update name in query
              "room":{'emission_value':0.003},#test value
              "small_fridge":{'emission_value':0.24383561643},#24 hours value - A++ fridge
              "medium_fridge":{'emission_value':0.31780821917},#24 hours value - A+ fridge
              "large_fridge":{'emission_value':0.47945205479},#24 hours value - A fridge
              "phone":{'emission_value':0.00005},#test value
              "pc_hour":{'emissions_value':0.0008},#test value
              "tv_hour":{'emissions_value':0.1133825079},#based on average use of plasma tv, hourly value
              "games_console_hour":{'emissions_value':0.0005},#test value
              "washer_hour":{'emission_value':0.27272727272},
              "dishwasher":{'emission_value':0.62222222222}, #per use
              "dryer_hour":{'emissions_value':1.07432432432},#per use
              "kettle_use":{'emissions_value':0.10311284046},#per use
              "other_uses":{'emissions_value':0.4}#arbitray value based on average of items above 
              }
              