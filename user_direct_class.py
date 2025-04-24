class direction_picklist():
    def __init__(self, page_direction, petrolCarChoices, dieselCarChoices, motorbikeChoices, accountChoices):
        self.page_direction = page_direction
        self.petrolCarChoices = petrolCarChoices
        self.dieselCarChoices = dieselCarChoices
        self.motorbikeChoices = motorbikeChoices
        self.accountChoices = accountChoices
        
        
    
    def petrolCarChoices(username):
        """Contains picklist for navigating petrol car related choices """
        import inquirer
        petrolDirect = [
            inquirer.List('Petrol Choice',
                          message = "Would you like to log a new emission or log a new average?",
                          choices = ["Log an emission", "Use a previous average", "Log a new average", "Go Back"]
                      )
            ]
        user_choice = inquirer.prompt(petrolDirect)
        direction = user_choice['Petrol Choice']
        if direction == "Log an emission":
            car_reg = input("Please input your car's registration number: ")
            from APIClass import API
            API.API_callout_for_calculator(username, car_reg)
        elif direction == "Use a previous average":
            from userClass import user
            user.useVehicleAverage(username)
        elif direction == "Log a new average":
            from APIClass import API
            API.gather_info_call_API(username)
        elif direction == "Go Back":
            direction_picklist.page_direction(username)
        else:
            print("Error encountered, invalid choice selected")
            exit
            
    def dieselCarChoices(username):
        """Contains picklist for navigating petrol car related choices """
        import inquirer
        dieselDirect = [
            inquirer.List('Diesel Choice',
                          message = "Would you like to log a new emission or log an average?",
                          choices = ["Log an emission", "Use a previous average", "Log a new average", "Go Back"]
                      )
            ]
        user_choice = inquirer.prompt(dieselDirect)
        direction = user_choice['Diesel Choice']
        if direction == "Log an emission":
            car_reg = input("Please input your car's registration number: ")
            from APIClass import API
            API.API_callout_for_calculator(username, car_reg)
        elif direction == "Use a previous average":
            from userClass import user
            user.useVehicleAverage(username)
        elif direction == "Log a new average":
            from APIClass import API
            API.gather_info_call_API(username)
        elif direction == "Go Back":
            direction_picklist.page_direction(username)
        else:
            print("Input not recognised, please try again")
            direction_picklist.page_direction(username)
            
    def motorbikeChoices(username):
        """Contains picklist for navigating motorbike related choices """
        import inquirer
        motorbikeDirect = [
            inquirer.List('Motorbike Choice',
                          message = "Would you like to log a new emission or log an average?",
                          choices = ["Log an emission", "Use a previous average", "Log a new average", "Go Back"]
                      )
            ]
        user_choice = inquirer.prompt(motorbikeDirect)
        direction = user_choice['Motorbike Choice']
        if direction == "Log an emission":
            motorbike_reg = input("Please input your bike's registration number: ")
            from APIClass import API
            API.API_callout_for_calculator(username, motorbike_reg)
        elif direction == "Use a previous average":
            from userClass import user
            user.useVehicleAverage(username)
        elif direction == "Log a new average":
            from APIClass import API
            API.gather_info_call_API(username)
        elif direction == "Go Back":
            direction_picklist.page_direction(username)
        else:
            print("Input not recognised, please try again")
            direction_picklist.page_direction(username)
    
    def accountChoices(username):
        """Contains picklist for managing a user's account"""
        import inquirer #import the inquirer module
        accountDirection = [ #initiate list
            inquirer.List('Account Choice', #calls the List class from inquirer
                          message = "Please select an option below", #prompt displayed to the user
                          choices = ["Change My Password", "Link An Account", "View My Link Requests", "Register a Vehicle", "Go Back"] #choices the user picks from
                      ),
            ]
        user_choice = inquirer.prompt(accountDirection) #calls the question and displays it for the user
        direction = user_choice['Account Choice'] #stores the user's answer to the question
        if direction == "Change My Password":
            from userClass import user
            user.change_password() #import user class and the change_password function
        elif direction == "Link An Account":
            from userClass import user #import user class and call the setLinkedUser function
            user.setLinkedUser(username)
        elif direction == "View My Link Requests":
            from userClass import user #import user class and call the approve_links function
            user.approve_links(username)
        elif direction == "Register a Vehicle":
            from registercar import vehicleCheck #imports the vehicleCheck function from registercar
            vehicleCheck(username)
        elif direction == "Go Back":
            direction_picklist.page_direction(username)
        else:
            print("Input not recognised, please try again")
            direction_picklist.page_direction(username)
            
    def appliance_choices (username): #logging appliance averages and ad-hoc logs
        import inquirer
        direct_question = [
            inquirer.List('Appliance Choice',
                          message = "Are you making a new average or logging an emission?",
                          choices = ["Making a New Average", "Logging a New Emission"]
                          )
            ]
        user_choice = inquirer.prompt(direct_question)
        direction = user_choice['Appliance Choice']
        if direction == "Making a New Average":
            from CreateDailyAverage import take_averages
            take_averages(username)
        elif direction == "Logging a New Emission":
            from ApplianceCalculator import retrieveAverage
            retrieveAverage(username)
        else:
            print("Choice not recognised, please try again")
            from user_direct_class import direction_picklist
            direction_picklist.page_direction(username)
    
    def page_direction(username): #the main menu
        """Contains picklist for navigating around major modules"""
        import inquirer
        direct_question = [
               inquirer.List('User Choice',
                             message = "Choose Task:",
                             choices = ["Log Petrol Car Emission", "Log Diesel Car Emission", "Log Motorbike Emission", "Appliance Emissions", "View Emission Graphs", "Manage My Account", "Go Back", "Log Out"]
                             #choices above direct users to each major module within the software
                          )
            ]

        user_choice = inquirer.prompt(direct_question)
        direction = user_choice['User Choice']
        if direction == "Log Petrol Car Emission":
            direction_picklist.petrolCarChoices(username) #call the petrol car sub menu
        elif direction == "Log Diesel Car Emission":
            direction_picklist.dieselCarChoices(username) #call the diesel car sub menu
        elif direction == "Log Motorbike Emission":
            direction_picklist.motorbikeChoices(username) #call the motorbike sub menu
        elif direction == "Appliance Emissions":
            direction_picklist.appliance_choices(username) #call appliance sub menu
        elif direction == "View Emission Graphs":
            from userClass import user #import the user class
            user.selectUserForTrending(username) #call the selectUserForTrending function
        elif direction == "Manage My Account":
            direction_picklist.accountChoices(username) #call the accountChoices sub menu
        elif direction == "Go Back":
            direction_picklist.page_direction(username)
        elif direction == "Log Out":
            exit #log out by terminating the application
        else:
            print("Error Encountered")
            exit #close the application due to an unknown error
            
