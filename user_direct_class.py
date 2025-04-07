class direction_picklist():
    def __init__(self, page_direction, petrolCarChoices, dieselCarChoices, motorbikeChoices):
        self.page_direction = page_direction
        self.petrolCarChoices = petrolCarChoices
        self.dieselCarChoices = dieselCarChoices
        self.motorbikeChoices = motorbikeChoices
        
    
    def petrolCarChoices(username):
        """Contains picklist for navigating petrol car related choices """
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
            
    def dieselCarChoices(username):
        """Contains picklist for navigating petrol car related choices """
        import inquirer
        dieselDirect = [
            inquirer.List('Diesel Choice',
                          message = "Would you like to log a new emission or log an average?",
                          choices = ["Log an emission", "Log an average"]
                      )
            ]
        user_choice = inquirer.prompt(dieselDirect)
        direction = user_choice['Diesel Choice']
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
            
    def motorbikeChoices(username):
        """Contains picklist for navigating motorbike related choices """
        import inquirer
        motorbikeDirect = [
            inquirer.List('Motorbike Choice',
                          message = "Would you like to log a new emission or log an average?",
                          choices = ["Log an emission", "Log an average"]
                      )
            ]
        user_choice = inquirer.prompt(motorbikeDirect)
        direction = user_choice['Motorbike Choice']
        if direction == "Log an emission":
            motorbike_reg = input("Please input your bike's registration number: ")
            from APIClass import API
            API.API_callout_for_calculator(username, motorbike_reg)
        elif direction == "Log an average":
            from APIClass import API
            API.gather_info_call_API(username)
        else:
            print("Error encountered")
            exit
    
    def accountChoices(username):
        """Contains picklist for managing a user's account"""
        import inquirer
        accountDirection = [
            inquirer.List('Account Choice',
                          message = "Please select an option below",
                          choices = ["Change My Password", "Link An Account", "View My Link Requests", "Register a Vehicle"]
                      ),
            ]
        user_choice = inquirer.prompt(accountDirection)
        direction = user_choice['Account Choice']
        if direction == "Change My Password":
            from userClass import user
            user.change_password()
        elif direction == "Link An Account":
            from userClass import user
            user.setLinkedUser(username)
        elif direction == "View My Link Requests":
            from userClass import user
            user.approve_links(username)
        elif direction == "Register a Vehicle":
            from registercar import vehicleCheck
            vehicleCheck(username)
        

    def page_direction(username): #the main menu
        """Contains picklist for navigating around major modules"""
        import inquirer
        direct_question = [
               inquirer.List('User Choice',
                             message = "Choose Task:",
                             choices = ["Log Petrol Car Emission", "Log Diesel Car Emission", "Log Motorbike Emission", "Log Appliance Emission", "View Emission Graphs", "Manage My Account", "Log Out"]
                             #choices above direct users to each major module within the software
                          )
            ]

        user_choice = inquirer.prompt(direct_question)
        direction = user_choice['User Choice']
        if direction == "Log Petrol Car Emission":
            direction_picklist.petrolCarChoices(username) #call the petrol car sub menu
        elif direction == "Log Diesel Car Emission":
            direction_picklist.dieselCarChoices #call the diesel car sub menu
        elif direction == "Log Motorbike Emission":
            direction_picklist.motorbikeChoices #call the motorbike sub menu
        elif direction == "Log Appliance Emission":
            from ApplianceCalculator import retrieveAverage
            retrieveAverage(username) #call the retrieveAverage function
        elif direction == "View Emission Graphs":
            from userClass import user #import the user class
            user.selectUserForTrending(username) #call the selectUserForTrending function
        elif direction == "Manage My Account":
            direction_picklist.accountChoices(username) #call the accountChoices sub menu
        elif direction == "Log Out":
            exit #log out by terminating the application
        else:
            print("Error Encountered")
            exit #close the application due to an unknown error
            
