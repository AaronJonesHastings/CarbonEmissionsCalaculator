"""
There are seven main GHGs that contribute to climate change, as covered by the Kyoto Protocol: carbon dioxide (CO2), methane (CH4),
nitrous oxide (N2O), hydrofluorocarbons (HFCs), perfluorocarbons (PFCs), sulphur hexafluoride (SF6) and nitrogen trifluoride (NF3).
Different activities emit different gases and you should report on the Kyoto Protocol GHG gases produced by your particular activities.											
All conversion factors presented here are in units of 'kilograms of carbon dioxide equivalent of Y per X' (kg CO2e of Y per X), 
where Y is the gas emitted and X is the unit activity.  CO2e is the universal unit of measurement to indicate the global warming 
potential (GWP) of GHGs, expressed in terms of the GWP of one unit of carbon dioxide. 											
"""
#Import relevant modules
import inquirer
from Dictionaries import motorbike_emission_dict

global motorbikeEmissionsValue
motorbikeEmissionsValue = 0

#establish motorbike switch value
motorbike = 0
#obtain motorbike type from user
motorbikeQuestions = [
    inquirer.List('Vehicle Type',
                  message = "Please select your vehicle type from the list",
                  choices =[ "Small Motorbike", "Medium Motorbike", "Large Motorbike", "Average Motorbike", "I do not have a motorbike"],
            ),
]

#store answer in motorbikeType variable
motorbikeAnswer = inquirer.prompt(motorbikeQuestions) #store answer
motorbikeType = (motorbikeAnswer["Vehicle Type"]) #store anwer in new variable to remove superfluous text

#print(motorbikeType)
#set switch value if the end user owns a motorbike
if motorbikeType != 'I do not have a motorbike':
    motorbike = 1
else:
    motorbike = 0

#initialise motorbikeEmission variable

if motorbike == 1:    

    motorbikeEmission = f"{motorbike_emission_dict[motorbikeType]['emission_value']}" #retrieve emission value from nested dictionary
    motorbikeEmission = float(motorbikeEmission) #store dictionary value as a float

    #get user input for minutes driven

    minutes = input(f"How many minutes have you driven {motorbikeType} today?\n") 
    minutes = int(minutes) #convert user input to interger for later manipulation

    #establish calculation for emissions

    def motorbikeEmissionCalculation(motorbikeEmission, minutes):
        if motorbike == 1:
             global motorbikeEmissionsValue
             emissionsPerMinute = motorbikeEmission / 60
             emissions = emissionsPerMinute * minutes
             print(f"Carbon emission output for this drive is {emissions}kgCO2e")
             motorbikeEmissionsValue = emissions
            

    motorbikeEmissionCalculation(motorbikeEmission, minutes) #run calculation
else:
   pass
