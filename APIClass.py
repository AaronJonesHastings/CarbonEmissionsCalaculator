from random import gammavariate


class API:
    def __init__ (self, key):
        self.key = key
    


    
    # Function to calculate distance between two postcodes, then calculate the emissions for that drive
    def calculate_distance_for_average(postcode1, postcode2, coords, car_reg, username, travel_mode="driving-car"):
        import openrouteservice
        from openrouteservice.directions import directions
        ORS_API_KEY = '5b3ce3597851110001cf6248aae0ceee7de14c67b09ed1f9fe6405a5'
        #print(coords)
        try:
            # Initialize OpenRouteService client
            client = openrouteservice.Client(key=ORS_API_KEY)
            routes = directions(client, coords)
            # Extract distance from the response (in meters)
            distance = routes["routes"][0]["summary"]["distance"]
            #duration = routes["routes"][0]["summary"]["duration"] #duration not needed but is returned by the API
            #print(f"The estimated distance in metres is {distance}") #distance in metres
            #print(routes)
        except openrouteservice.exceptions.ApiError as e:
            print(f"API Error: {e}")
            return None
        #convert metres into miles - 1 metre = 0.000621371 miles
        miles = 0.000621371
        if distance > 0:
            distance_miles = distance*miles
            print(f"The estimated distance in miles is {distance_miles}")
            """
            now calculate emissions based on the distance and emission value for the chosed vehicle
            """
            #retrieve vehicle details from SQL table so nested dictionary can be queried
            import dbConnection
            cursor = dbConnection.db.cursor()
            sql1 = "SELECT registration_number FROM vehicle_details WHERE registration_number = %s" #SQL query to check car exists
            sql2 = "SELECT owner FROM vehicle_details WHERE registration_number = %s" #SQL query to get owner
            cursor.execute(sql1, (car_reg,))
            car_exists = cursor.fetchone()
            #print(car_reg) #for testing
            #print(car_exists) #for testing
            if car_reg in car_exists:
                cursor.execute(sql2, (car_reg,))
                owner_check = cursor.fetchone()
                if type(car_exists) != type(None):
                    if username in owner_check:
                        sql3 = "SELECT mpg, type FROM vehicle_details WHERE registration_number = %s"
                        cursor.execute(sql3, (car_reg,))
                        searchResults = cursor.fetchall()
                        #print(searchResults)
                        mpg, carType = searchResults[0]
                        #print(mpg)
                        #print(carType)
                        """
                        Now select the relevant dictionary based on car vehicle type. Motorbikes are covered by the phrase
                        carType for simplicity in coding
                        """
                        if "Petrol" in carType:
                            #print("Petrol dict used") #test print
                            from Dictionaries import petrol_emission_dict
                            carEmission = f"{petrol_emission_dict[carType]['emission_value']}" #retrieve emission value from nested dictionary
                            carEmission = float(carEmission) #store dictionary value as a float
                        elif "Diesel" in carType:
                            #print("Diesel dict used") #test print
                            from Dictionaries import diesel_emission_dict
                            carEmission = f"{diesel_emission_dict[carType]['emission_value']}"
                            carEmission = float(carEmission)
                        else:
                            #print("Mototbike dict used") #test print
                            from Dictionaries import motorbike_emission_dict
                            carEmission = f"{motorbike_emission_dict[carType]['emission_value']}"
                            carEmission = float(carEmission)
                        
                        """ Calculate Emission """
                        #Emission algorithm = (distance/mpg) * emission factor
                        fuelUsed = distance_miles / mpg
                        drive_emission = fuelUsed * carEmission
                        print(f"Total emissions for this drive are {drive_emission} CO2e")
                        import inquirer
                        query_save = [
                            inquirer.List('Save Drive',
                                          message = "Would you like to save this drive?",
                                          choices = ["Yes", "No"],
                                      ),
                            ]
                        
                        query_answer = inquirer.prompt(query_save)
                        choice = query_answer['Save Drive']
                        if choice == "Yes":
                            drive_name = input("Please provide a name for this drive: ")
                            sql4 = "INSERT INTO drive_averages (user, vehicle_reg, starting_postcode, ending_postcode, distance, drive_emission, drive_name) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                            val = (username, car_reg, postcode1, postcode2, distance, drive_emission, drive_name)
                            cursor.execute(sql4, val)
                            dbConnection.db.commit()
                            print("Drive saved")
                            from user_direct_class import direction_picklist
                            direction_picklist.page_direction(username)
                        else:
                             exit
                    else:
                        print("You are not the owner of this vehicle, please try again with a car egistered to this account")
                        from user_direct_class import direction_picklist
                        direction_picklist.page_direction(username)
                else:
                    print("Error encountered, please try again")
                    from user_direct_class import direction_picklist
                    direction_picklist.page_direction(username)
            else:
                print("Car not found, please try again")
                from user_direct_class import direction_picklist
                direction_picklist.page_direction(username)
        else:
            print("Invalid distance for this journey, please try again with new postcodes")
            from user_direct_class import direction_picklist
            direction_picklist.page_direction(username)

        #carEmission = f"{petrol_emission_dict[carType]['emission_value']}" #retrieve emission value from nested dictionary
        #carEmission = float(carEmission) #store dictionary value as a float
        
    #def store_drive_average(postcode1, postode2, distane_miles, username, car_reg, emission_value):
        

    def gather_info_call_API(username):
        import dbConnection #import for cursors
        mycursor = dbConnection.db.cursor()
        sql = "SELECT username FROM user_details WHERE username = %s"
        mycursor.execute(sql, (username,))
        result = mycursor.fetchone()
        if result:
            """ Gather Postcodes and Vehicle Reg """
            starting_postcode = input('Please enter your starting postcode: ')
            if len(starting_postcode) > 7:
                print("Postcode is too long, please try again")
                exit
            
            ending_postcode = input('Please enter your ending postcode: ')

            if len(ending_postcode) > 7:
                print("Postcode is too long, please try again")
                exit  
                
            car_reg = input('Please enter the registration number of your vehicle: ')
            if len(car_reg) < 7: #if reg too short
                print("Car registration too short, please enter again")
                exit
            elif len(car_reg) > 7: #reg too long - break down the reg, remove the space, and combine again
                reg_list = []
                reg_list = car_reg.split() #split reg in the middle (using the space) and store both parts in a list
                car_reg = reg_list[0]+reg_list[1] #combine both elements
                car_reg = car_reg.upper() #make upper case
                
            else:
                car_reg = car_reg.upper() #make upper case
                #print(car_reg)
                #make sure car reg is formatted correctly for SQL query
            
            """ Use geopy to convert postcodes to latitude/longitude values """
            
            from geopy.geocoders import Nominatim
        
            geolocator = Nominatim(user_agent="postcode_to_coordinates")
            start_location = geolocator.geocode(starting_postcode)
            end_location = geolocator.geocode(ending_postcode)
            if start_location:
                #return (location.longitude, location.latitude)
                #print(f'{start_location.longitude}, {start_location.latitude}')
                start_coords = [start_location.longitude, start_location.latitude]
                #print(start_coords) #test print for validation
            else:
                raise ValueError(f"Could not find location for postcode: {starting_postcode}, please try again")
                from APIClass import API
                API.gather_info_call_API(username)
                exit
            if end_location:
                #print(f'{end_location.longitude}, {end_location.latitude}')
                end_coords = [end_location.longitude, end_location.latitude]
                #print(end_coords)
            else:
                raise ValueError(f"Could not find location for postcode: {ending_postcode}")
                from APIClass import API
                API.gather_info_call_API(username)
            
            coords = (start_coords, end_coords)
            API.calculate_distance_for_average(starting_postcode, ending_postcode, coords, car_reg, username)
        
        else:
            print("User not found, please log out try again")
            from login import verify_password
            verify_password()
            exit
    



    def API_callout_for_calculator(username, car_reg):
        import dbConnection #import for cursors
        mycursor = dbConnection.db.cursor()
        sql = "SELECT username FROM user_details WHERE username = %s"
        mycursor.execute(sql, (username,))
        result = mycursor.fetchone()
        if result:
            """ Gather Postcodes and Vehicle Reg """
            starting_postcode = input('Please enter your starting postcode: ')
            if len(starting_postcode) > 7:
                print("Postcode is too long, please try again")
                exit
            
            ending_postcode = input('Please enter your ending postcode: ')

            if len(ending_postcode) > 7:
                print("Postcode is too long, please try again")
                exit  
                
            if len(car_reg) < 7: #if reg too short
                print("Car registration too short, please enter again")
                exit
            elif len(car_reg) > 7: #reg too long - break down the reg, remove the space, and combine again
                reg_list = []
                reg_list = car_reg.split() #split reg in the middle (using the space) and store both parts in a list
                car_reg = reg_list[0]+reg_list[1] #combine both elements
                car_reg = car_reg.upper() #make upper case
                #print(f"Car reg after splits is {car_reg}") #testing
                
            else:
                car_reg = car_reg.upper() #make upper case
                #make sure car reg is formatted correctly for SQL query
                
            """ Use geopy to convert postcodes to latitude/longitude values """
            
            from geopy.geocoders import Nominatim
        
            geolocator = Nominatim(user_agent="postcode_to_coordinates")
            start_location = geolocator.geocode(starting_postcode)
            end_location = geolocator.geocode(ending_postcode)
            if start_location:
                #return (location.longitude, location.latitude)
                #print(f'{start_location.longitude}, {start_location.latitude}')
                start_coords = [start_location.longitude, start_location.latitude]
                #print(start_coords) #test prints
            else:
                raise ValueError(f"Could not find location for postcode: {starting_postcode}")
                exit
            if end_location:
                #print(f'{end_location.longitude}, {end_location.latitude}')
                end_coords = [end_location.longitude, end_location.latitude]
                #print(end_coords) #test prints
            else:
                raise ValueError(f"Could not find location for postcode: {ending_postcode}")
            coords = (start_coords, end_coords)
            import openrouteservice
            from openrouteservice.directions import directions
            ORS_API_KEY = '5b3ce3597851110001cf6248aae0ceee7de14c67b09ed1f9fe6405a5'
            #print(coords)
            try:
                # Initialize OpenRouteService client
                client = openrouteservice.Client(key=ORS_API_KEY)
                routes = directions(client, coords)
                # Extract distance from the response (in meters)
                distance = routes["routes"][0]["summary"]["distance"]
                #duration = routes["routes"][0]["summary"]["duration"] #duration not needed but is returned by the API
                #print(f"The estimated distance in metres is {distance}") #distance in metres
                #print(routes)
            except openrouteservice.exceptions.ApiError as e:
                print(f"API Error: {e}")
                return None
            #convert metres into miles - 1 metre = 0.000621371 miles
            miles = 0.000621371
            if distance > 0:
                distance_miles = distance*miles
                print(f"The estimated distance in miles is {distance_miles}")
                #now find the vehicle type to import the corret calculator
                sql_vehicle_type = "SELECT type FROM vehicle_details WHERE registration_number = %s"
                #print(type(sql_vehicle_type)) #testing
                val = (car_reg)
                #print(car_reg) #test print
                #print(type(val)) #testing
                mycursor.execute(sql_vehicle_type, (val,))
                result = mycursor.fetchone()
                #print(result)
                if result is not None:
                    if "Petrol" in result[0]:
                        from PetrolCarCalculator import car_check
                        car_check(username, distance_miles, car_reg)
                    elif "Motorbike" in result[0]: #run motorbike first in-case of diesel motorbike
                        from MotorbikeCalculator import motorbike_check
                        motorbike_check(username, distance_miles, car_reg)
                    elif "Diesel" in result[0]:
                        from DieselCarCalculator import car_check
                        car_check(username, distance_miles, car_reg)
                    else:
                        print("Car not found, please try again")
                        from user_direct_class import direction_picklist
                        direction_picklist.page_direction(username)
                        exit
                else:
                    print("Error enountered, please try again")
                    from user_direct_class import direction_picklist
                    
                    direction_picklist.page_direction(username)
                    exit
                
                
#API.gather_info_call_API('Admin') #for testing