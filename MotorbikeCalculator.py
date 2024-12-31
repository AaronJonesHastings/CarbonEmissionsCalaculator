#Import relevant modules
#import inquirer
from Dictionaries import motorbike_emission_dict #import motorbike dictionary
import dbConnection
from datetime import date


#establish global variables for future use

motorbikeEmissionsValue = 0
#establish motorbike reg variable
global motorbike_reg
motorbike_reg = ()
#establish motorbike switch value, made global so nested_motorbike_check can update it
global motorbike
motorbike = 0
#establish motorbikeType variable
global motorbikeType
motorbikeType = ()

"""
create the function that checks the emissions of a motorbike
This will be called by the check_motorbike function
"""

def motorbikeEmissionsCalculation(username, motorbike_reg, motorbike, motorbikeType):
        if motorbike == 1:
            motorbikeEmission = f"{motorbike_emission_dict[motorbikeType]['emission_value']}" #retrieve emission value from nested dictionary
            motorbikeEmission = float(motorbikeEmission) #store dictionary value as a float

            #get user input for minutes driven

            minutes = input(f"How many minutes have you driven {motorbike_reg} today?\n") 
            minutes = int(minutes) #convert user input to interger for later manipulation
            
            global motorbikeEmissionsValue 
            emissionsPerMinute = motorbikeEmission / 60
            emissions = emissionsPerMinute * minutes
            print(f"Carbon emission output for your drive of {motorbike_reg} is {emissions}kgCO2e")
            motorbikeEmissionsValue = emissions
            print(motorbikeEmissionsValue)
            today = date.today()
            """
            Now establish details to be passed to mysql, including: username, motorbiketype,
            reg number, emissions
            """
            mycursor = dbConnection.db.cursor()
            sql = "INSERT INTO car_emissions (user, date, vehicle, value) VALUES (%s, %s, %s, %s)"
            val = (username, today, motorbike_reg, motorbikeEmissionsValue)
            mycursor.execute(sql, val)
            dbConnection.db.commit()
            print(mycursor.rowcount, "record inserted")
        else:
            print("Error encountered")

#define variable used to remove excess characters from a returned SQL query

def strip_and_replace(variable):
    variable = str(variable).strip('(),')
    variable = variable.replace("'", "")            
            
#create the function that checks for if a user has a bike registered against their username

def motorbike_check(username):
    motorbike_reg = input("Please enter your bike's registration number: ")
    cursor = dbConnection.db.cursor()
    sql1 = "SELECT registration_number FROM vehicle_details WHERE registration_number = %s" #SQL query to pass
    sql2 = "SELECT owner FROM vehicle_details WHERE registration_number = %s" #SQL query to get owner
    cursor = dbConnection.db.cursor() #get cursor from dbConnection.py
    cursor.execute(sql1, (motorbike_reg,)) #execute the sql1 query
    motorbike_exists = cursor.fetchone() #store sql1 result in variable
    cursor.execute(sql2, (motorbike_reg,)) #execute sql2 query
    owner_check = cursor.fetchone() #store sql2 query in variable
    #print(owner_check) #to test SQL return
    #print(motorbike_exists) #to test SQL return
    
    #Perform check to see if the motorbike submitted is in the vehicle_details table
    #If yes - pass information to the calculator function
    
    if type(motorbike_exists) != type(None): #check for none type - if none type then no return from mysql
        #SQL returns values formatted as ('Username',) so have to check if the variable is contained in the result
        if username in owner_check:
            username = username
            motorbike_reg = motorbike_reg
            motorbike = 1 #set switch to pass to calculation function
            sql3 = "SELECT type FROM vehicle_details WHERE registration_number = %s" #sql to retrieve motorbike type
            cursor.execute(sql3, (motorbike_reg,)) #execute sql3 query
            motorbikeType = cursor.fetchone() #store sql3 query in a variable
            #clean excess characters from the sql query
            motorbikeType = str(motorbikeType).strip('(),')
            motorbikeType = motorbikeType.replace("'", "")
            motorbikeEmissionsCalculation(username, motorbike_reg, motorbike, motorbikeType)
        else:
            print("You are not the owner of this vehicle")
    else:
        print("This motorbike does not exist, please register the vehicle to log these emissions")
        from registercar import vehicleCheck
        vehicleCheck(username)
        
def strip_and_replace(variable):
    variable = str(variable).strip('(),')
    variable = variable.replace("'", "")

username = input("Please provide your username: ")
motorbike_check(username)