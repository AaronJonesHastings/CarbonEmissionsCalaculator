import dbConnection
import inquirer
#from Dictionaries import users_cars

#define function for motorbike registration
def register_motorbike(username):
    cursor = dbConnection.db.cursor()
    sql = "SELECT username FROM user_details WHERE username = %s" #SQL query to pass
    cursor = dbConnection.db.cursor() #get cursor from dbConnection.py
    cursor.execute(sql, (username,)) #execute the SQL
    result = cursor.fetchone() #store restult in variable

    if result:
       bike_reg = input("Please provide your motorbike's registration number: ")
       if len(bike_reg) < 7: #if reg too short
            print("Bike registration too short, please enter again")
            exit
       elif len(bike_reg) > 7: #reg too long - break down the reg, remove the space, and combine again
            reg_list = []
            reg_list = bike_reg.split() #split reg in the middle (using the space) and store both parts in a list
            bike_reg = reg_list[0]+reg_list[1] #combine both elements
            bike_reg = bike_reg.upper() #make upper case
       else:
            bike_reg = bike_reg.upper() #make upper case      
       bike_reg = bike_reg.upper() #format correctly
       bike_make = input("Please provide your make of motorbike: ")
       bike_model = input("Please provide the model of your motorbike: ")

       bike_question = [
       inquirer.List('Bike Type',
                      message = "Please select your bike type from the list",
                      choices = [ "Small Motorbike", "Medium Motorbike", "Large Motorbike", "Average Motorbike"],
                      ),
       ]
       
       #store answer
       bike_answer = inquirer.prompt(bike_question)
       petrol_type = "Petrol"
       bike_type = (bike_answer['Bike Type'])
       mpg = input("Please provide the mpg value for your car.\nIf you are unsure this can be viewed here: https://www.fuelly.com/car")
       try:
            float(mpg)
       except ValueError:
            print("MPG value must be numeric.\nPlease try again")
            exit
       owner = username
       mycursor = dbConnection.db.cursor()
       sql = "INSERT INTO vehicle_details (registration_number, make, model, type, petrol_type, mpg, owner) VALUES (%s, %s, %s, %s, %s, %s, %s)"
       val = (bike_reg, bike_make, bike_model, bike_type, petrol_type, mpg, owner)
       mycursor.execute(sql, val)
       dbConnection.db.commit()
       print(mycursor.rowcount, "record inserted")
    else:
        print("Account does not exist")

#define function for car registration
def registercar(username):
    cursor = dbConnection.db.cursor()
    sql = "SELECT username FROM user_details WHERE username = %s" #SQL query to pass
    cursor = dbConnection.db.cursor() #get cursor from dbConnection.py
    cursor.execute(sql, (username,)) #execute the SQL
    result = cursor.fetchone() #store restult in variable

    if result:
        car_reg = input("Please provide your car registration number: ")
        car_reg = car_reg.upper()
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
        car_make = input("Please provide your make of car: ")
        car_model = input("Please provide the model of your car: ")
        #establish input questions for vehicle and petrol types
        car_question = [
            inquirer.List('Vehicle Type',
                      message = "Please select your vehicle type from the list",
                      choices =[ "Small Car - Petrol", "Medium Car - Petrol", "Large Car - Petrol", "Average Car - Petrol", "Mini - Petrol",
                                "Supermini - Petrol", "Executive - Petrol", "Sports - Petrol", "Dual Purpose 4X4 - Petrol", "MPV - Petrol",
                                "Small Car - Diesel", "Medium Car - Diesel", "Large Car - Diesel", "Average Car - Diesel", "Mini - Diesel",
                                "Supermini - Diesel", "Executive - Diesel", "Sports - Diesel", "Dual Purpose 4X4 - Diesel", "MPV - Diesel"],
                ),
        ]
        #store answers
        car_answer = inquirer.prompt(car_question)
        choice = (car_answer['Vehicle Type'])
        if "Petrol" in choice:
            petrol_type = "Petrol"
        else:
            petrol_type = "Diesel"
        #extract the relevant bit of the answers
        car_type = (car_answer['Vehicle Type'])
        owner = username
        #print(car_reg)
        #print(car_make)
        #print(car_model)
        #print(car_type)
        #print(petrol_type)
        #establish mpg value - taken from fuelly website for test purposes - https://www.fuelly.com/car    
        mpg = input("Please provide the mpg value for your car.\nIf you are unsure this can be viewed here: https://www.fuelly.com/car")
        try:
            float(mpg)
        except ValueError:
            print("MPG value must be numeric.\nPlease try again")
            exit
        mycursor = dbConnection.db.cursor()
        sql = "INSERT INTO vehicle_details (registration_number, make, model, type, petrol_type, mpg, owner) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (car_reg, car_make, car_model, car_type, petrol_type, mpg, owner)
        mycursor.execute(sql, val)
        dbConnection.db.commit()
        print(mycursor.rowcount, "record inserted")
    else:
        print("Account does not exist")

#Check if user already exists
def vehicleCheck(username):        
       
    cursor = dbConnection.db.cursor() #get cursor from dbConnection.py
    sql = "SELECT username FROM user_details WHERE username = %s" #SQL query to pass
    cursor.execute(sql, (username,)) #execute the SQL
    result = cursor.fetchone() #store restult in variable
    if result: #if user exists
        insert_type = input("Would you like to register a car or a bike?: ") #check which function to run
        if insert_type == "Car" or insert_type == "car":
            registercar(username) #execute function
        else:
            register_motorbike(username) #execute function
    else:
        print("Username does not exist") #failed SQL query
        

username = "Admin"
vehicleCheck(username)