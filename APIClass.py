from turtle import exitonclick


class API:
    def __init__ (self, key):
        self.key = key
    
    """   
    def call_api(starting_postcode, ending_postcode, car_reg, username): #used to create lat/long co-ordinates for API call
        from geopy.geocoders import Nominatim
        geolocator = Nominatim(user_agent="postcode_to_coordinates")
        start_location = geolocator.geocode(starting_postcode)
        end_location = geolocator.geocode(ending_postcode)
        if start_location:
            #return (location.latitude, location.longitude)
            print(f'{start_location.latitude}, {start_location.longitude}')
        else:
            raise ValueError(f"Could not find location for postcode: {starting_postcode}")
            exit
        if end_location:
            print(f'{end_location.latitude}, {end_location.longitude}')
        else:
            raise ValueError(f"Could not find location for postcode: {ending_postcode}")
        exit
    """    
    
    # Function to calculate distance between two postcodes
    def calculate_distance(coords1, coords2, username, car_reg, travel_mode="driving-car"):
        import openrouteservice
        key =  '5b3ce3597851110001cf6248aae0ceee7de14c67b09ed1f9fe6405a5'
        client = openrouteservice.Client(key=key)

               
        # Make a request to the OpenRouteService API
        try:
            route = client.directions(
                coordinates=[coords1, coords2],
                profile=travel_mode,
                format="json"
            )
            # Extract distance from the response (in meters)
            distance = route["routes"][0]["summary"]["distance"]
            duration = route["routes"][0]["summary"]["duration"]
            
            print(distance)
            print(duration)
            return {
                "distance_km": distance / 1000,  # Convert to kilometers
                "duration_minutes": duration / 60  # Convert to minutes
            }
        except openrouteservice.exceptions.ApiError as e:
            print(f"API Error: {e}")
            return None


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
                #make sure car reg is formatted correctly for SQL query
            
            """ Use geopy to convert postcodes to latitude/longitude values """
            
            from geopy.geocoders import Nominatim
        
            geolocator = Nominatim(user_agent="postcode_to_coordinates")
            start_location = geolocator.geocode(starting_postcode)
            end_location = geolocator.geocode(ending_postcode)
            if start_location:
                #return (location.latitude, location.longitude)
                #print(f'{start_location.latitude}, {start_location.longitude}')
                start_coords = [start_location.latitude, start_location.longitude]
            else:
                raise ValueError(f"Could not find location for postcode: {starting_postcode}")
                exit
            if end_location:
                #print(f'{end_location.latitude}, {end_location.longitude}')
                end_coords = [end_location.latitude, end_location.longitude]
            else:
                raise ValueError(f"Could not find location for postcode: {ending_postcode}")
            
            #print(start_coords, end_coords)
            #print(type(start_coords))
            start_coords = tuple(start_coords)
            #print(type(start_coords))
            #print(start_coords)
            end_coords = tuple(end_coords)
            API.calculate_distance(start_coords, end_coords, username, car_reg)
        
        else:
            exit

API.gather_info_call_API('Admin')