class direction_picklist():
    def __init__(self, page_direction):
        self.page_direction = page_direction
    
    def petrolCarChoices(username):
        import inquirer
        petrolDirect = [
            inquirer.List('Petrol Choice',
                          message = "Would you like to log a new emission or log an average?",
                          choices = ["Log an emission", "Log an average"]
                      )
            ]
        user_choice = inquirer.prompt(petrolDirect)
        direction = user_choice['Petrol Choice']
        if direction == "Log an emission":
            car_reg = input("Please input your car's registration number: ")
            from APIClass import API
            API.API_callout_for_calculator(username, car_reg)
        elif direction == "Log an average":
            from APIClass import API
            API.gather_info_call_API(username)
        else:
            print("Error encountered")
            exit
    
    def page_direction(username):
        import inquirer
        direct_question = [
               inquirer.List('User Choice',
                             message = "Choose Task:",
                             choices = ["Log Petrol Car Emission", "Log Diesel Car Emission", "Log Motorbike Emission", "Log Appliance Emission", "View Emission Graphs", "Log Out"]
                          )
            ]

        user_choice = inquirer.prompt(direct_question)
        direction = user_choice['User Choice']
        if direction == "Log Petrol Car Emission":
            direction_picklist.petrolCarChoices(username)
        elif direction == "Log Diesel Car Emission":
            from DieselCarCalculator import car_check
            car_check(username)
        elif direction == "Log Motorbike Emission":
            from MotorbikeCalculator import motorbike_check
            motorbike_check(username)
        elif direction == "Log Appliance Emission":
            from ApplianceCalculator import retrieveAverage
            retrieveAverage(username)
        elif direction == "View Emission Graphs":
            from userClass import user
            user.sortAllData(username)
        elif direction == "Log Out":
            exit
        else:
            print("Error Encountered")
            exit
            
