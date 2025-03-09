class direction_picklist():
    def __init__(self, page_direction):
        self.page_direction = page_direction

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
            from PetrolCarCalculator import car_check
            car_check(username)
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
            
        
        