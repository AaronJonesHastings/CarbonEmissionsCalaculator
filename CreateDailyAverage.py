#estbalish variables for take_avergaes function to reference

import inquirer

global username
global oven
global oven_type
global bulb_type
global rooms
global hours_lit
global fridge_size
global heating_hours
global number_phones
global pc_hours
global tv_hours
global games_console_hours
global washer_hours
global dryer_hours
global kettle_uses
global other_hours
global user_average

def calculate_average(oven, oven_type, bulb_type, rooms, hours_lit, fridge_size, heating_hours, number_phones, pc_hours, tv_hours, games_console_hours, washer_hours, dryer_hours, dishwasher_hours, kettle_uses, other_hours, user):
    
    """Take input from "tage_averges" function,uses it to query the applicance dictionary, and converts any
    numerical data to a float for manipulation. This is then added to the daily_averages table """
    
    from Dictionaries import appliances #import dictionaries.py for value referencing
    import inquirer
    
    """ Oven Calculation"""
    
    oven_emission = f"{appliances[oven_type]['emission_value']}" #retrieve emission value from nested dictionary using oven_type variable
    float(oven_emission)
    oven = float(oven)
    oven_emission = float(oven_emission)
    total_oven_emissions = oven*oven_emission #multiply oven (hours) with oven_emission (kwh)
    print(f"Oven emissions = {total_oven_emissions}")
    
    """Bulb Calculaion"""
    
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
    
    """Dishwasher Calculation"""
    dishwasher_emission = f"{appliances["dishwasher"]['emission_value']}"
    dishwasher_hours = float(dishwasher_hours)
    dishwasher_emission = float(dishwasher_emission)
    dishwasher = dishwasher_hours*dishwasher_emission
    print(f"Dishwasher emissions = {dishwasher}")
    
    """Others Calculation"""
    other_emissions = f"{appliances["other_uses"]['emissions_value']}"
    other_hours = float(other_hours)
    other_emissions = float(other_emissions)
    other = other_emissions*other_hours
    print(f"Other emissions = {other}")



    total_emissions_calc = total_oven_emissions + fridge_emission + total_bulb_emission + heating_emission + phones + pc + tv + console + washer + dryer + dishwasher + kettle + other
    total_emissions_calc = float(total_emissions_calc)
    print(f"The total emissions value is {total_emissions_calc}")
    
    """Input to SQL Table"""
    #establish connection
    import dbConnection
    #check that the user exists
    cursor = dbConnection.db.cursor() #get cursor from dbConnection.py
    sql = "SELECT username FROM user_details WHERE username = %s" #SQL query to pass
    cursor.execute(sql, (user,)) #execute the SQL
    result = cursor.fetchone() #store restult in variable
    if result:
        #check if user already has an entry in the daily_averages tables
        sql = "SELECT user FROM daily_averages WHERE user = %s"
        val = (user,)
        cursor.execute(sql, val)
        result = cursor.fetchone()
        if result:
            override_check = input("You already have a registered daily average, would you like to override this? Please enter Yes or No: ")
            if override_check == "Yes" or override_check == "yes":
                sql = "UPDATE daily_averages SET user = %s, oven = %s, bulb_type = %s, rooms = %s, hours_lit = %s, fridge_size = %s, heating_hours = %s, number_phones = %s, pc_hours = %s, tv_hours = %s, washer_hours = %s, dryer_hours = %s, dishwasher_hours = %s, games_console_hours = %s, kettle_uses = %s, other_hours = %s, total_daily_emission = %s WHERE user = %s"
                values = (user, oven, bulb_type, rooms, hours_lit, fridge_size, heating_hours, number_phones, pc_hours, tv_hours, washer_hours, dryer_hours, dishwasher_hours, games_console_hours, kettle_uses, other_hours, total_emissions_calc, user)
                cursor.execute(sql, values)
                dbConnection.db.commit()
                print(cursor.rowcount, "record updated")
            else:
                print("You changes have been discarded")
        else:
            sql = "INSERT INTO daily_averages (user, oven, oven_type, bulb_type, rooms, hours_lit, fridge_size, heating_hours, number_phones, pc_hours, tv_hours, washer_hours, dryer_hours, dishwasher_hours, games_console_hours, kettle_uses, other_hours, total_daily_emission) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (user, oven, oven_type, bulb_type, rooms, hours_lit, fridge_size, heating_hours, number_phones, pc_hours, tv_hours, washer_hours, dryer_hours, dishwasher_hours, games_console_hours, kettle_uses, other_hours, total_emissions_calc)
            cursor.execute(sql, values)
            dbConnection.db.commit()
            print(cursor.rowcount, "record inserted")
            from user_direct_class import direction_picklist
            direction_picklist.page_direction(user)
    else:
        print("Error encountered")

def take_averages(username):
    print("You will be asked a series of questions. We ask that you provide an honest, average account of your daily activity. These values will be used to calculate your average daily emissions value going forwards, unless you choose to change it")
    user = username
    
    #establish oven details
    oven_question = [
        inquirer.List('Oven Type',
                      message = "Do you use a gas or electric oven?",
                      choices = ["Gas", "Electric"],
        ),
    ]
    
    oven_answer = inquirer.prompt(oven_question)
    choice = oven_answer['Oven Type']
    if choice == "Gas":
        oven_type = "gas_oven"
    else:
        oven_type = "electric_oven"
    
    oven = input("How many hours a day do you use your oven?\n")
    
    #create picklist for bulb type
    bulb_question = [
        inquirer.List('bulb type',
                      message = "Please select your type of bulb",
                      choices = ["Energy Saving Bulbs", "Standard Bulb"],
        ),
    ]
    
    bulb_answer = inquirer.prompt(bulb_question)
    if bulb_answer == "Energy Saving Bulbs":
        bulb_type = "energy_saving_bulb"
    else:
        bulb_type = "standard_bulb"
    
    rooms = input("How many rooms do you light in your house?\n")
    hours_lit = input("On average, for how many hours do you keep each room lit for?\n")
    
    #establish fridge type using picklist
    fridge_question = [
        inquirer.List('Fridge Type',
                      message = "Do you have a small, medium or large fridge-freezer?",
                      choices = [ "Small", "Medium", "Large"],
        ),
    ]
    fridge_answer = inquirer.prompt(fridge_question) #take picklist answer
    
    #convert answer into the dictionary equivalent
    if fridge_answer == "Small":
        fridge_size = "small_fridge"
    elif fridge_answer == "Medium":
        fridge_size = "medium_fridge"
    else:
        fridge_size = "large_fridge"
    
    heating_hours = input("How many hours do you heat your home for?\n")
    number_phones = input("How many mobile phones are charged daily in your house?\n")
    pc_hours = input("How many hours a day is a PC or laptpop used in your house?\n")
    tv_hours = input("How many hours a day is a tv used in your house?\n")
    games_console_hours = input("How many hours a day is a games console used in your house?\n")
    washer_hours = input("How many hours a day is a washing machine used in your house?\n")
    dryer_hours = input("How many hours a day is a dryer used in your house?\n")
    dishwasher_hours = input("How many hours a day is a dishwasher used in your house?\n")
    kettle_uses = input("How many times a day is a kettle boiled in your house?\n")
    other_hours = input("How many hours a day, cumulatively, are other appliances used in your house?\n")
    
    
    #call calculation function
    calculate_average(oven, oven_type, bulb_type, rooms, hours_lit, fridge_size, heating_hours, number_phones, pc_hours, tv_hours, games_console_hours, washer_hours, dishwasher_hours, dryer_hours, kettle_uses, other_hours, user)
    
    
#print("You will be asked a series of questions. We ask that you provide an honest, average account of your daily activity")

#username = "BigWizard"
#take_averages(username)