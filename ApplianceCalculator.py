from Dictionaries import appliances
import dbConnection
import inquirer
from datetime import date
import datetime

"""
In the UK, 1 kWh is equal to roughly 265g of Co2
The ukIntensity variable stores the latest figures
for the UK, taken from the UK government for
2023, and converts 1kWh to the KG of Co2 equivalent
"""
ukIntensity = 0.207074288590604

def upload_average(oven, bulb_type, rooms, hours_lit, fridge_size, heating_hours, number_phones, pc_hours, tv_hours, washer_hours, dryer_hours, games_console_hours, kettle_uses, other_hours, total_daily_emissions):
    """
    Receives information from rerieve average and uploads to the mysql server
    using a similar method to CreateDailyAverage.py
    """
    
    oven_emission = appliances["oven"]['emission_value'] #retrieve emission value from nested dictionary
    """ Oven Calculation"""
    float(oven_emission)
    oven = float(oven)
    total_oven_emissions = oven*oven_emission #multiply oven (hours) with oven_emission (kwh)
    print(f"Oven emissions = {total_oven_emissions}")
    
    """Lighting Calculaion"""
    bulb_emission = f"{appliances[bulb_type]['emission_value']}"
    bulb_emission = float(bulb_emission)
    rooms = float(rooms) #convert to float
    hours_lit = float(hours_lit) #convert to float
    total_bulb_emission = (rooms*hours_lit)*bulb_emission
    print(f"Bulb emissions = {total_bulb_emission}")
    
    """Fridge Calculation"""
    fridge_emission = f"{appliances[fridge_size]['emission_value']}" #no calculation needed, dict stores a 24 hour value
    fridge_emission = float(fridge_emission)
    print(f"Fridge emissions = {fridge_emission}")
    
    """Heating Calculation"""
    room_value = f"{appliances["room"]['emission_value']}"
    room_value = float(room_value)
    heating_hours = float(heating_hours)
    heating_emission = heating_hours*(rooms*room_value)
    print(f"Heating emissions = {heating_emission}")
    
    """Phones Calculation"""
    phone_emissions = f"{appliances["phone"]['emission_value']}"
    number_phones = float(number_phones)
    phone_emissions = float(phone_emissions)
    phones = number_phones*phone_emissions
    print(f"Phone emissions = {phones}")
    
    """PC Calculation"""
    pc_emission = f"{appliances["pc_hour"]['emissions_value']}"
    pc_hours = float(pc_hours)
    pc_emission = float(pc_emission)
    pc = pc_emission*pc_hours
    print(f"PC emissions = {pc}")
    
    """TV Calculation"""
    tv_emission = f"{appliances["tv_hour"]['emissions_value']}"
    tv_hours = float(tv_hours)
    tv_emission = float(tv_emission)
    tv =tv_emission*tv_hours
    print(f"TV emissions = {tv}")
    
    """Console Calculation"""
    games_emission = f"{appliances["games_console_hour"]['emissions_value']}"
    games_console_hours = float(games_console_hours)
    games_emission = float(games_emission)
    console = games_emission*games_console_hours
    print(f"Console emissions = {console}")
    
    """Washer Calculation"""
    washer_emission = f"{appliances["washer_hour"]['emission_value']}"
    washer_hours = float(washer_hours)
    washer_emission = float(washer_emission)
    washer = washer_emission*washer_hours
    print(f"Washer emissions = {washer}")
    
    """Dryer Calculation"""
    dryer_emission = f"{appliances["dryer_hour"]['emissions_value']}"
    dryer_hours = float(dryer_hours)
    dryer_emission = float(dryer_emission)
    dryer = dryer_emission*dryer_hours
    print(f"Dryer emissions = {dryer}")
    
    """Kettle Calculation"""
    kettle_emission = f"{appliances["kettle_use"]['emissions_value']}"
    kettle_uses = float(kettle_uses)
    kettle_emission = float(kettle_emission)
    kettle = kettle_emission*kettle_uses
    print(f"Kettle emissions = {kettle}")
    
    """Others Calculation"""
    other_emissions = f"{appliances["other_uses"]['emissions_value']}"
    other_hours = float(other_hours)
    other_emissions = float(other_emissions)
    other = other_emissions*other_hours
    print(f"Other emissions = {other}")
    
    total_emissions_calc = total_oven_emissions + fridge_emission + total_bulb_emission + heating_emission + phones + pc + tv + console + washer + dryer + kettle + other
    total_emissions_calc = float(total_emissions_calc)
    print(f"The total emissions value is {total_emissions_calc}")
    
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
    
    cursor = dbConnection.db.cursor() #get cursor from dbConnection.py
    sql = "SELECT username FROM user_details WHERE username = %s" #SQL query to pass
    cursor.execute(sql, (username,)) #execute the SQL
    result = cursor.fetchone() #store restult in variable
    if result:
        #check if user already has an entry in the daily_averages tables
        sql = "INSERT INTO appliance_logs (total_emissions, date, oven, lighting, fridge, heating, phones, pc, tv, games_console, washer, dryer, kettle, other, user) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (total_emissions_calc, date_of_emission, total_oven_emissions, total_bulb_emission, fridge_emission, heating_emission, phones, pc, tv, console, washer, dryer, kettle, other, username )
        cursor.execute(sql, val)
        dbConnection.db.commit()
        print(cursor.rowcount, "record inserted")
    else:
        print("Error encountered, please try again")
        

def createEmissionCalculation(username):
    
    cursor = dbConnection.db.cursor() #get cursor from dbConnection.py
    sql = "SELECT username FROM user_details WHERE username = %s" #SQL query to pass
    cursor.execute(sql, (username,)) #execute the SQL
    result = cursor.fetchone() #store restult in variable
    #print(result)
    if result:
        #establish emission date
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
     
        sql = "SELECT rooms, fridge_size, bulb_type FROM daily_averages WHERE user = %s" #retrieve basline data for dictionary reference
        val = username
        cursor.execute(sql, (val,))
        result = cursor.fetchall()
        print(result)
        row = result[0]
        rooms = row[0]
        fridge_size = row[1]
        bulb_type = row[2]
        #begin collecting user input    
        oven = input("For how many hours have you used your oven/stove? ")
        hours_lit = input("For how many hours did you light your house for? ")
        hours_heated = input("For how many hours did you heat your house for? ")
        number_phones = input("How many phones were charged in your house? ")
        hours_pc = input("For how many hours were PCs used in your house? ")
        hours_tv = input("For how many hours was a TV on in your house? ")
        hours_washer = input("How many hours was a washing machine used for in your house? ")
        hours_dryer = input("How many hours was a dryer used for in your house? ")
        hours_console = input("For how many hours was a games console used in your house? ")
        kettle_uses = input("How mnay times was a kettle boiled in your house? ")
        hours_other = input("Cummulatively, for how many hours were other appliances used in your house? ")

        #begin calculations

        """Oven Calculation"""
        oven = float(oven)
        oven_emission = appliances["oven"]['emission_value']
        oven_emission = float(oven_emission)
        total_oven = oven*oven_emission

        """Lighting Calclulation"""
        rooms = float(rooms) #retrieved from earlier sql query
        bulb_emission = f"{appliances[bulb_type]['emission_value']}"
        bulb_emission = float(bulb_emission)
        hours_lit = float(hours_lit)
        total_bulb = rooms*(hours_lit*bulb_emission)
        
        """Fridge Calculation"""
        total_fridge = f"{appliances[fridge_size]['emission_value']}" #no calculation needed, dict stores a 24 hour value
        total_fridge = float(total_fridge)

        """Heating Calculation"""
        room_emission = f"{appliances["room"]['emission_value']}"
        hours_heated = float(hours_heated)
        room_emission = float(room_emission)
        total_heating = rooms*(hours_heated*room_emission) #rooms already a float, see lighting calculation
        
        """Phones Calculation"""
        phone_emissions = f"{appliances["phone"]['emission_value']}"
        number_phones = float(number_phones)
        phone_emissions = float(phone_emissions)
        total_phones = phone_emissions*number_phones
        
        """PC Calculation"""
        pc_emission = f"{appliances["pc_hour"]['emissions_value']}"
        hours_pc = float(hours_pc)
        pc_emission = float(pc_emission)
        total_pc = pc_emission*hours_pc
        
        """TV Calculation"""
        tv_emission = f"{appliances["tv_hour"]['emissions_value']}"
        hours_tv = float(hours_tv)
        tv_emission = float(tv_emission)
        total_tv = tv_emission*hours_tv
        
        """Console Calculation"""
        games_emission = f"{appliances["games_console_hour"]['emissions_value']}"
        hours_console = float(hours_console)
        games_emission = float(games_emission)
        total_console = games_emission*hours_console

        """Washer Calculation"""
        washer_emission = f"{appliances["washer_hour"]['emission_value']}"
        hours_washer = float(hours_washer)
        washer_emission = float(washer_emission)
        total_washer = hours_washer*washer_emission
        
        """Dryer Calculation"""
        dryer_emission = f"{appliances["dryer_hour"]['emissions_value']}"
        hours_dryer = float(hours_dryer)
        dryer_emission = float(dryer_emission)
        total_dryer = hours_dryer*dryer_emission

        """Kettle Calculation"""
        kettle_emission = f"{appliances["kettle_use"]['emissions_value']}"
        kettle_uses = float(kettle_uses)
        kettle_emission = float(kettle_emission)
        total_kettle = kettle_emission*kettle_uses
        
        """Others Calculation"""
        other_emissions = f"{appliances["other_uses"]['emissions_value']}"
        hours_other = float(hours_other)
        other_emissions = float(other_emissions)
        total_other = hours_other*other_emissions

        """Final Calculation"""
        final_emissions = total_oven + total_bulb + total_fridge + total_heating + total_phones + total_tv + total_console + total_washer + total_dryer + total_kettle + total_other #adds all final calculations above
        
        """Import into SQL"""
        sql = "SELECT total_emissions FROM appliance_logs WHERE user = %s AND date = %s"
        val = (username, date_of_emission)
        cursor.execute(sql, val)
        result = cursor.fetchone()
        
        if result:
            update_question = [
                inquirer.List ('overrideCheck',
                               message = "An entry for this date already exists, would you like to override this?",
                               choices = ["Yes", "No"],
                ),
            ]
            
            update_answer = inquirer.prompt(update_question)
            choice = update_answer['overrideCheck']
            
            if  choice == "Yes":
                overrideSql = "UPDATE appliance_logs SET total_emissions = %s, date = %s, oven = %s, lighting = %s, fridge = %s, heating = %s, phones = %s, pc = %s, tv = %s, games_console = %s, washer = %s, dryer = %s, kettle = %s, other = %s, user = %s WHERE user = %s AND date = %s"    
                overrideVals = (final_emissions, date_of_emission, total_oven, total_bulb, total_fridge, total_heating, total_phones, total_pc, total_tv, total_console, total_washer, total_dryer, total_kettle, total_other, username, username, date_of_emission)
                cursor.execute(overrideSql, overrideVals)
                dbConnection.db.commit()
                print(cursor.rowcount, "record updated")
            else:
                print("Update discarded")
                exit()

        else:
            sql = "INSERT INTO appliance_logs (total_emissions, date, oven, lighting, fridge, heating, phones, pc, tv, games_console, washer, dryer, kettle, other, user) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (final_emissions, date_of_emission, total_oven, total_bulb, total_fridge, total_heating, total_phones, total_pc, total_tv, total_console, total_washer, total_dryer, total_kettle, total_other, username)
            cursor.execute(sql, val)
            dbConnection.db.commit()
            print(cursor.rowcount, "record inserted")
    else:
        print("No average found, please establish your average daily emissions")
        from CreateDailyAverage import take_averages
        take_averages(username)



def retrieveAverage(username):

    #determine if user's average should be used for the day's emission calculation
    average_question = [
        inquirer.List ('use_average',
                       message = "Would you like to use your stored average?",
                       choices = [ "Yes", "No"],
        ),
    ]

    average_answer = inquirer.prompt(average_question)
    
    choice = (average_answer['use_average'])
    if choice == "Yes":
        
        cursor = dbConnection.db.cursor() #get cursor from dbConnection.py
        sql = "SELECT total_daily_emission FROM daily_averages WHERE user = %s"
        val = (username,)
        cursor.execute(sql, val,)
        result = cursor.fetchone()
        if result:
            sql2 = "SELECT oven, bulb_type, rooms, hours_lit, fridge_size, heating_hours, number_phones, pc_hours, tv_hours, washer_hours, dryer_hours, games_console_hours, kettle_uses, other_hours, total_daily_emission FROM daily_averages WHERE user = %s"
            val2 = (username,)
            cursor.execute(sql2, val2)
            result = cursor.fetchall()
            row = result[0]
            oven = row[0]
            bulb_type = row[1]
            rooms = row[2]
            hours_lit = row[3]
            fridge_size = row[4]
            heating_hours = row[5]
            number_phones = row[6]
            pc_hours = row[7]
            tv_hours = row[8]
            washer_hours = row[9]
            dryer_hours = row[10]
            games_console_hours = row[11]
            kettle_uses = row[12]
            other_hours = row[13]
            total_daily_emissions = row[14]
            
            upload_average(oven, bulb_type, rooms, hours_lit, fridge_size, heating_hours, number_phones, pc_hours, tv_hours, washer_hours, dryer_hours, games_console_hours, kettle_uses, other_hours, total_daily_emissions)
        
    else:
        createEmissionCalculation(username)
        
    """ Check if user wants to do another upload """
    repeat_question = [
    inquirer.List ('repeat_input',
               message = "Would you like to log more appliance emissions?",
               choices = [ "Yes", "No"],
        ),
    ]

    repeat_answer = inquirer.prompt(repeat_question)
    
    choice = (repeat_answer['repeat_input'])
    if choice == "Yes":
        retrieveAverage(username)
    else:
        exit
        
        
username = "Admin"
retrieveAverage(username)