class Vehicle:
    """
    To initiate the Vehicle class, containing concetpts and methods
    for vehicles such as their calculations, and child classes depending
    on the type of vehicle
    """
    
    def __init__ (self, registration_number, make, model, vehicleType, petrol_type, owner):
        #correspond to entries in the vehcile_details sql table
        self.registration_number = registration_number
        self.make = make
        self.model = model
        self.type = vehicleType
        self.petrol_type = petrol_type
        self.owner = owner
    
    
class petrolCar(Vehicle): #child of the Vehicle class
    def __init__(self, registration_number, make, model, carType, petrol_type, owner):
        #initialise attributes specific to petrolCars
        self.registration_number = registration_number
        self.make = make
        self.model = model
        self.type = carType
        self.petrol_type = petrol_type
        self.owner = owner
        
    def carEmissionsCalculation(username, registration_number, car, carType): #CREATE CHECKS FOR SQL INJECTION SAFETY
        if car == 1:
            
            import dbConnection
            from datetime import date
            from Dictionaries import petrol_emission_dict
            carEmission = f"{petrol_emission_dict[carType]['emission_value']}" #retrieve emission value from nested dictionary
            carEmission = float(carEmission) #store dictionary value as a float

            #get user input for minutes driven

            minutes = input(f"How many minutes have you driven {registration_number} today?\n") #CREATE CODE TO CONFIRM THIS IS A FLOAT. CREATE LENGTH CHECK
            minutes = float(minutes) #convert user input to float for later manipulation
            
            global petrolCarEmissionsValue 
            emissionsPerMinute = carEmission / 60
            emissions = emissionsPerMinute * minutes
            print(f"Carbon emission output for your drive of {registration_number} is {emissions}kgCO2e")
            petrolCarEmissionsValue = emissions
            print(petrolCarEmissionsValue)
            
            today = date.today()
            """
            Now establish details to be passed to mysql, including: username, cartype,
            reg number, emissions
            """
            mycursor = dbConnection.db.cursor()
            sql = "INSERT INTO car_emissions (user, date, vehicle, value) VALUES (%s, %s, %s, %s)"
            val = (username, today, registration_number, petrolCarEmissionsValue)
            mycursor.execute(sql, val)
            dbConnection.db.commit()
            print(mycursor.rowcount, "record inserted")
        else:
            print("Error encountered")
        
    def car_check(username):
        import dbConnection
        registration_number = input("Please enter your car's registration number: ")
        cursor = dbConnection.db.cursor()
        sql1 = "SELECT registration_number FROM vehicle_details WHERE registration_number = %s" #SQL query to pass
        sql2 = "SELECT owner FROM vehicle_details WHERE registration_number = %s" #SQL query to get owner
        cursor = dbConnection.db.cursor() #get cursor from dbConnection.py
        cursor.execute(sql1, (registration_number,)) #execute the sql1 query
        car_exists = cursor.fetchone() #store sql1 result in variable
        cursor.execute(sql2, (registration_number,)) #execute sql2 query
        owner_check = cursor.fetchone() #store sql2 query in variable
        #print(owner_check) #to test SQL return
        #print(car_exists) #to test SQL return
    
        #Perform check to see if the car submitted is in the vehicle_details table
        #If yes - pass information to the calculator function
    
        if type(car_exists) != type(None): #check for none type - if none type then no return from mysql
        #SQL returns values formatted as ('Username',) so have to check if the variable is contained in the result
            if username in owner_check:
                username = username
                #car_reg = car_reg
                car = 1 #set switch to pass to calculation function
                sql3 = "SELECT type FROM vehicle_details WHERE registration_number = %s" #sql to retrieve car type. Safer as value is taken from mysql
                cursor.execute(sql3, (registration_number,)) #execute sql3 query
                carType = cursor.fetchone() #store sql3 query in a variable
                #clean excess characters from the sql query
                carType = str(carType).strip('(),')
                carType = carType.replace("'", "")
                petrolCar.carEmissionsCalculation(username, registration_number, car, carType)
            else:
                print("You are not the owner of this vehicle")
        else:
            print("This car does not exist, please register the vehicle to log these emissions")
            from registercar import vehicleCheck
            vehicleCheck(username)
    


class dieselCar(Vehicle): #child of the Vehicle class
    def __init__(self, registration_number, make, model, carType, petrol_type, owner):
        #initialise attributes specific to diesel cars
        self.registration_number = registration_number
        self.make = make
        self.model = model
        self.type = carType
        self.petrol_type = petrol_type
        self.owner = owner

class motorbike(Vehicle): #child of the Vehcile class
    def __init__(self, registration_number, make, model, bikeType, petrol_type, owner):
        #initialise attributes specific to motorbikes
        self.registration_number = registration_number
        self.make = make
        self.model = model
        self.type = bikeType
        self.petrol_type = petrol_type
        self.owner = owner

username = "Admin"

petrolCar.car_check(username)