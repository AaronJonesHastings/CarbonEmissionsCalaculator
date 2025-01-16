#Import relevant modules
#import inquirer
from Dictionaries import petrol_emission_dict #import car type dictionary
#from Dictionaries import users_cars #import nested dictionary containing cars registered to users
import dbConnection
from datetime import date
import vehicleClass #not yet in use, will be used of OOP purposes later


#establish global variables for future use

petrolCarEmissionsValue = 0
#establish car reg variable
global car_reg
car_reg = ()
#establish car switch value, made global so nested_car_check can update it
global car
car = 0
#establish carType variable
global carType
carType = ()

"""
create the function that checks the emissions of a car
This will be called by the check_car function
"""

def carEmissionsCalculation(username, car_reg, car, carType): #CREATE CHECKS FOR SQL INJECTION SAFETY
        if car == 1:
            import inquirer
            import datetime
            carEmission = f"{petrol_emission_dict[carType]['emission_value']}" #retrieve emission value from nested dictionary
            carEmission = float(carEmission) #store dictionary value as a float

            #get user input for minutes driven

            minutes = input(f"How many minutes have you driven {car_reg} for this drive?\n") #CREATE CODE TO CONFIRM THIS IS A FLOAT. CREATE LENGTH CHECK
            minutes = float(minutes) #convert user input to float for later manipulation
            
            global petrolCarEmissionsValue 
            emissionsPerMinute = carEmission / 60
            emissions = emissionsPerMinute * minutes
            print(f"Carbon emission output for your drive of {car_reg} is {emissions}kgCO2e")
            petrolCarEmissionsValue = emissions
            print(petrolCarEmissionsValue)
            date_question = [
            inquirer.List('Date of Emission',
                          message = "Was ths emission from today?",
                          choices = [ "Yes","No"],
                ),
            ]
    
            date_answer = inquirer.prompt(date_question)
    
            choice = date_answer['Date of Emission']
     
            if choice == "Yes":
                date_of_emission = date.today()
            else:
                date_of_emission = input("Please input the date of these emissions: ")
                date_of_emission = datetime.datetime.strptime(date_of_emission, "%d/%m/%Y")
            """
            Now establish details to be passed to mysql, including: username, cartype,
            reg number, emissions
            """
            mycursor = dbConnection.db.cursor()
            sql = "INSERT INTO car_emissions (user, date, vehicle, value) VALUES (%s, %s, %s, %s)"
            val = (username, date_of_emission, car_reg, petrolCarEmissionsValue)
            mycursor.execute(sql, val)
            dbConnection.db.commit()
            print(mycursor.rowcount, "record inserted")
        else:
            print("Error encountered")

#define variable used to remove excess characters from a returned SQL query

def strip_and_replace(variable):
    variable = str(variable).strip('(),')
    variable = variable.replace("'", "")            
            
#create the function that checks for if a user has a car registered against their username

def car_check(username):
    #take car reg
    while True:
        car_reg = input("Please enter your car's registration number: ")
        if len(car_reg) < 7:
            print("Car registration too short, please enter again")
        elif len(car_reg) > 8:
            print("Car registration is too long, please enter again")
        else:
            break
    #make sure car reg is formatted correctly for SQL query
    car_reg = car_reg.upper()
    print(car_reg) #for testing purposes
        
    cursor = dbConnection.db.cursor()
    sql1 = "SELECT registration_number FROM vehicle_details WHERE registration_number = %s" #SQL query to pass
    sql2 = "SELECT owner FROM vehicle_details WHERE registration_number = %s" #SQL query to get owner
    cursor = dbConnection.db.cursor() #get cursor from dbConnection.py
    cursor.execute(sql1, (car_reg,)) #execute the sql1 query
    car_exists = cursor.fetchone() #store sql1 result in variable
    cursor.execute(sql2, (car_reg,)) #execute sql2 query
    owner_check = cursor.fetchone() #store sql2 query in variable
    #print(owner_check) #to test SQL return
    #print(car_exists) #to test SQL return
    
    #Perform check to see if the car submitted is in the vehicle_details table
    #If yes - pass information to the calculator function
    
    if type(car_exists) != type(None): #check for none type - if none type then no return from mysql
        #SQL returns values formatted as ('Username',) so have to check if the variable is contained in the result
        if username in owner_check:
            username = username
            car_reg = car_reg
            car = 1 #set switch to pass to calculation function
            sql3 = "SELECT type FROM vehicle_details WHERE registration_number = %s" #sql to retrieve car type. Safer as value is taken from mysql
            cursor.execute(sql3, (car_reg,)) #execute sql3 query
            carType = cursor.fetchone() #store sql3 query in a variable
            #clean excess characters from the sql query
            carType = str(carType).strip('(),')
            carType = carType.replace("'", "")
            carEmissionsCalculation(username, car_reg, car, carType)
        else:
            print("You are not the owner of this vehicle")
    else:
        print("This car does not exist, please register the vehicle to log these emissions")
        from registercar import vehicleCheck
        vehicleCheck(username)
        
def strip_and_replace(variable):
    variable = str(variable).strip('(),')
    variable = variable.replace("'", "")

username = input("Please provide your username: ")
car_check(username)