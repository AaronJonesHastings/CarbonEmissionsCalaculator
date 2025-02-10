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
    def calculate_distance(postcode1, postcode2, coords, car_reg, username, travel_mode="driving-car"):
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
            duration = routes["routes"][0]["summary"]["duration"]
            print(distance)
            #print(routes)
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
                #return (location.longitude, location.latitude)
                #print(f'{start_location.longitude}, {start_location.latitude}')
                start_coords = [start_location.longitude, start_location.latitude]
                print(start_coords)
            else:
                raise ValueError(f"Could not find location for postcode: {starting_postcode}")
                exit
            if end_location:
                #print(f'{end_location.longitude}, {end_location.latitude}')
                end_coords = [end_location.longitude, end_location.latitude]
                print(end_coords)
            else:
                raise ValueError(f"Could not find location for postcode: {ending_postcode}")
            
            coords = (start_coords, end_coords)
            API.calculate_distance(starting_postcode, ending_postcode, coords, username, car_reg)
        
        else:
            exit

API.gather_info_call_API('Admin')