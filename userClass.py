global vehicleEmissions
global applianceEmissions
global vehicleEmissionDates
global applianceEmissionDates
vehicleEmissions = []
applianceEmissions = []
vehicleEmissionDates = []
applianceEmissionDates = []

class user:
    """
    Class used to define user traits
   and contain define user specific methods
   
   change_password - for use when a user intentionally wants to change a password
   forgot_password - for use when a user does not know their password
   lockout - set lockout value to 1 (true) in SQL tabel if login attempts exceeded
   """
    def __init__(self, username, forename, surname, dob, password, email):
        #initiate user concepts - concepts match columns in the user_details SQL table
        #most are not in use but they are included in-case they are useful later
        self.username = username
        self.forename = forename
        self.surname = surname
        self.dob = dob
        self.password = password
        self.email = email
    
    def change_passsword():
        """For use when a user knows their password and wishes to pick a new one"""    
          
        import dbConnection #import for cursors
        mycursor = dbConnection.db.cursor()
        import bcrypt #for encrypting the password
        username = input("Please enter your username: ")
        sql = "SELECT username FROM user_details WHERE username = %s"
        mycursor.execute(sql, (username,))
        result = mycursor.fetchone()
        print(f"The affected user will be {result}")
        if result:
            currentPassword = input("Please provide your current password: ")
            sql = "SELECT password FROM user_details WHERE username = %s" #SQL query to pass
            #mycursor = dbConnection.db.cursor() #get cursor from dbConnection.py
            mycursor.execute(sql, (username,)) #execute the SQL. Passing named parameters for safety (SQL injections)
            result2 = mycursor.fetchone() #store restult in variable
            #print(f"The second SQL query retuend {result2}") #old test

            if result2:
                stored_hash = result2[0].encode('utf-8') #get hash in bytes
                #now verify the password against the stored hash
                if bcrypt.checkpw(currentPassword.encode('utf-8'), stored_hash):
                    import string
                    import getpass
                    while True:
                        newPassword = getpass.getpass("Please enter your chosen password:\n")
                        is_valid = all(( #check all 4 conditions below are met
                            len(newPassword) >= 8,#check character length is at least 8 
                            any(c.isalpha() for c in newPassword), #checks for the presence of an alpha character
                            any(c.isdigit() for c in newPassword), #checks for a numeric character
                            any(c in string.punctuation for c in newPassword) #checks for a special character
                        ))
                        if is_valid:
                            break
                        print("Password must contain a number and special character, and be at least 8 characters long\n")
                    verify_password = getpass.getpass("Please enter your password again:\n")
                    if newPassword != verify_password:                   
                        print("Your chosen password does not match, please try again.")
                        user.change_password()
                    else:
                        #hash newPassword variable and upload
                        salt = bcrypt.gensalt()
                        hashed_password = bcrypt.hashpw(newPassword.encode('utf-8'), salt)
                        sql = "UPDATE user_details SET password = %s WHERE username = %s"
                        val = (hashed_password, username)
                        mycursor.execute(sql, val)
                        dbConnection.db.commit()
                        print("Password successfully updated")
                        print(f"Rows affected: {mycursor.rowcount}")
                else:
                    print("Password incorrect, please contact support or use the 'forgot password' option")
                    return
            else:
                print("Unexpexted connectivity error encountered, please try again")
                user.change_password()
        else:
            print("Error: user not found, please try again or contact support")
            return
    
    def forgot_password():
        #used when a user does not know their password
        import dbConnection
        mycursor = dbConnection.db.cursor()
        username = input("Please enter your username:\n")
        #email = input("Please enter your email address:\n")
        sql = "SELECT email FROM user_details WHERE username = %s" #this way round in-case someone has multiple email addresses
        val = (username,)
        mycursor.execute(sql, val)
        result = mycursor.fetchone()
        if result:
            sq_query = "SELECT security_question FROM user_details WHERE username = %s" #fetch security question
            mycursor.execute(sq_query, val)
            result2 = mycursor.fetchone()
            #remove excess formatting from query return
            result2clean = str(result2).strip('(),')
            result2clean = result2clean.replace("'", "")
            print(f"Please answer the following question:\n{result2clean}")
            answer = input()
            sa_query = "SELECT security_answer FROM user_details WHERE username =%s"
            mycursor.execute(sa_query, val,)
            sa_answer = mycursor.fetchone()
            #remove excess formatting from answer
            saClean = str(sa_answer).strip('(),')
            saClean = saClean.replace("'", "")
            if answer == saClean:
                import bcrypt
                import getpass #used to hide password input
                import string
                while True:
                    newPassword = getpass.getpass("Please enter your chosen password:\n")
                    is_valid = all(( #check all 4 conditions below are met
                        len(newPassword) >= 8,#check character length is at least 8 
                        any(c.isalpha() for c in newPassword), #checks for the presence of an alpha character
                        any(c.isdigit() for c in newPassword), #checks for a numeric character
                        any(c in string.punctuation for c in newPassword) #checks for a special character
                    ))
                    if is_valid:
                        break
                    print("Password must contain a number and special character, and be at least 8 characters long\n")
                verify_password = getpass.getpass("Please enter your password again:\n")
                if newPassword != verify_password:                   
                    print("Your chosen password does not match, please try again.")
                    user.forgot_password()
                else:
                    #hash newPassword variable and upload
                    salt = bcrypt.gensalt()
                    hashed_password = bcrypt.hashpw(newPassword.encode('utf-8'), salt)
                    locked = 0
                    sql = "UPDATE user_details SET password = %s, locked = %s WHERE username = %s"
                    val = (hashed_password, locked, username)
                    mycursor.execute(sql, val,)
                    dbConnection.db.commit()
                    print("Password successfully updated")
                    print(f"Rows affected: {mycursor.rowcount}")
                    from user_direct_class import direction_picklist
                    direction_picklist.page_direction(username)
            else:
                print("Your answer does not match our reords. Please contact support for further assistance, or try again.")
                exit
        else:
            print("No user found, please try again")
            exit
            
    def unlockAccount(username):
        import dbConnection
        mycursor = dbConnection.db.cursor()
        sq_query = "SELECT security_question FROM user_details WHERE username = %s" #fetch security question
        val = (username, )
        mycursor.execute(sq_query, val)
        result2 = mycursor.fetchone()
        #remove excess formatting from query return
        result2clean = str(result2).strip('(),')
        result2clean = result2clean.replace("'", "")
        print(f"Please answer the following question:\n{result2clean}")
        answer = input()
        sa_query = "SELECT security_answer FROM user_details WHERE username =%s"
        mycursor.execute(sa_query, val,)
        sa_answer = mycursor.fetchone()
        #remove excess formatting from answer
        saClean = str(sa_answer).strip('(),')
        saClean = saClean.replace("'", "")
        if answer == saClean:
            unlockSQL = "UPDATE user_details SET locked = 0 WHERE username = %s"
            val = (username, )
            mycursor.execute(unlockSQL, val)
            dbConnection.db.commit()
            print("Account Unlocked\nReturning user to login page")
            from login import verify_password
            login_attempts = 0
            verify_password(username, login_attempts)
            
    def lockout(username):
        import dbConnection
        sql = "UPDATE user_details SET locked = %s WHERE username = %s" #set the lockout status to "1! in SQL server
        locked = '1'
        val = (locked, username)
        mycursor = dbConnection.db.cursor()
        mycursor.execute(sql, val) #execute sql statement
        dbConnection.db.commit() #commit the change
        print("Account locked due to too many inorrect password entries. Please contact support to unlock your account, or select forgot password") #print error message for the user
        import inquirer
        lockout_question = [
            inquirer.List ('Unlock Choices',
                           message = 'Please select unlock acount, forgotten password or close application:',
                           choices = ["Forgotten password", "Unlock account", "Close application"],
                       ),
            ]
            
        account_management_answer = inquirer.prompt(lockout_question)
        account_choice = (account_management_answer['Unlock Choices']) #allow users to select their next action
        if account_choice == "Forgotten password":
            from userClass import user
            user.forgot_password() #initiate the forgotten password sequence - i.e. change password
        elif account_choice == "Unlock account":
            from userClass import user
            user.unlockAccount(username) #initiate the unlock sequence - which will change the lockout status to 0 after passing security checks
        elif account_choice == "Close application":
            exit #exit the application
        
    def graphAppliances(username, applianceEmissions, applianceEmissionDates):
        import matplotlib.pyplot as plt
        #separate out dates and floats in the emission lists returned from retrieveEmissions function
        plt.plot (applianceEmissionDates, applianceEmissions)
        #set title and labels
        plt.title("Appliance Emissions Trending") #graph title
        plt.xlabel("Date") #x axis label
        plt.xticks(rotation=45)
        plt.ylabel("Co2 Emissions") #y axis label
        
        plt.grid(True)
        plt.show() #show the graph
        
    def graphVehicles(username, vehicleEmissions, vehicleEmissionDates):
        import matplotlib.pyplot as plt
        #separate out dates and floats in the emission lists returned from retrieveEmissions function
        plt.plot (vehicleEmissionDates, vehicleEmissions)
        plt.title("Vehicle Emissions Trending")
        plt.xlabel("Date")
        plt.xticks(rotation=45)
        plt.ylabel("Co2 Emissions")
        plt.grid(True)
        plt.show()
        
    def totalGraphing(username, totalEmissions, totalEmissionsDates):
        import matplotlib.pyplot as plt
        from matplotlib import style
        #separate out dates and floats in the emission lists returned from retrieveEmissions function
        plt.plot (totalEmissionsDates, totalEmissions)
        plt.title("Total Emissions Trending")
        plt.xlabel("Date")
        plt.xticks(rotation=45)
        plt.ylabel("Co2 Emissions Per Day (kg)")
        style.use("ggplot")
        plt.grid(True)
        plt.show()
        from user_direct_class import direction_picklist
        direction_picklist.page_direction(username)
        
    def selectUserForTrending(username):
        import inquirer
        query_user  = [
            inquirer.List('User For Trending',
                      message = f"Would you like to view your data or a linked user's?",
                      choices = ["My own", "A linked user's"],
                  ),
            ]
        query_answer = inquirer.prompt(query_user)
        choice = query_answer['User For Trending']
        if choice == "My own": #i.e. if viewing your own data
            user.retrieveEmissionsWithDate(username) #initiate graphing process
        #now to handle how to import a linked account's data
        else:
            import dbConnection
            cursor = dbConnection.db.cursor()
            sql = "SELECT linked_accounts FROM user_details WHERE username = %s" #retrieve linked accounts from the SQL table
            val = (username,)
            cursor.execute(sql, val)
            linked_accounts = [] #initiate list to store account options in
            linked_results = cursor.fetchall()
            #print(linked_results) #debugging
            for item in linked_results:
                linked_accounts = [u.strip() for u in item[0].split(',') if u.strip()]
            #print(linked_accounts)
            linked_accounts = linked_results[0][0].lstrip(', ').split(', ') #clean data, stip leading commas and store in the linked_accounts list
            #linked_accounts = list(dict.fromkeys(linked_accounts)) #remove any duplication, mmay not be needed
            #print(linked_accounts) #debugging
            """Now to allow the user to select the account to import data for"""
            #import colorama
            #from colorama import just_fix_windows_console
            from pick import pick
            title = "Select a username:"
            selected_account, _ = pick(linked_accounts, title)
            #just_fix_windows_console()
            print(f"You have selected: {selected_account}")
            linked_user = selected_account.strip(' ,')
            print(linked_user)
            #now call the retrieveEmissionsWithDate function
            user.retrieveEmissionsWithDate(linked_user)

    def retrieveEmissionsWithDate(username):
        import dbConnection
        from datetime import date
        mycursor = dbConnection.db.cursor()
        """retrieve all emissions from the appliance_logs and car_emissions table and store them in separate lists"""
        #create lists for storing emission returns
        global applianceEmissions
        applianceEmissions = []
        global vehicleEmissions
        vehicleEmissions = []
        
        #SQL query for appliance emission values
        applianceSQL = "SELECT total_emissions, date FROM appliance_logs WHERE user = %s"
        val = (username,) #val to be used for car and appliance queries
        mycursor.execute(applianceSQL, val)
        applianceResult = mycursor.fetchall() #store SQL returns
        #print(f"Appliance Results:\n{applianceResult}") #test print
        #print("Total number of appliance emission records = ", mycursor.rowcount) #test print

        #iterate through the result and add to the emissionResults list
        n = 0
        for i in applianceResult:
            applianceEmissions.append(applianceResult[n])
            n = n+1
        #print(f"After appending, applianceEmissions =\n{applianceEmissions}")
        #print(applianceEmissions)

        #SQL query for car emissions
        vehicleSQL = "SELECT value, date FROM car_emissions WHERE user = %s"
        mycursor.execute(vehicleSQL, val,)
        vehicleResult = mycursor.fetchall()
        #print(f"Vehicle Result is:\n{vehicleResult}") #test print
        #print("Total number of vehcile emissions = ", mycursor.rowcount) #test print

        #iterate through vehcicle emission returns and store in vehicleEmissions
        n = 0
        for i in vehicleResult:
            vehicleEmissions.append(vehicleResult[n])
            n = n+1
        #print(f"After appending, vehicleEmissions =\n{vehicleEmissions}") #test print
        #print(vehicleEmissions)
             
        data = vehicleEmissions #store data in separate lists
        #print("Separated Data")
        
        sorted_data = sorted(data, key=lambda x: x[1]) #vehicle data after sorting
        
        vehicleEmissionDates = [item[1] for item in sorted_data] #separate dates from emissions
        vehicleEmissionDates = [date.isoformat(item) for item in vehicleEmissionDates] #format dates appropriately
        #print(f"Vehicle Emission Dates are:\n{vehicleEmissionDates}") #test print
        
        
        vehicleEmissions = [item[0] for item in sorted_data] #take emission values, not dates
        #print(f"Vehicle Emissions are:\n{vehicleEmissions}") #test print
        
       
        #repeat above for appliance emissions
        data2 = applianceEmissions
        sorted_data2 = sorted(data2, key=lambda x: x[1])
        applianceEmissionDates = [item[1] for item in sorted_data2]
        applianceEmissionDates = [date.isoformat(item) for item in applianceEmissionDates]
        applianceEmissions = [item[0] for item in sorted_data2]
        #print(f"Appliance emissions are:\n{applianceEmissions}") #test print
        #print(f"Appliance emission dates are:\n{applianceEmissionDates}") #test print
        

        
        """ 
        #Test merging appliance and vehicle values - no longer needed as this is carried out by the sortAllData function
        
        from collections import defaultdict
        combinedEmissions = defaultdict(float) #used for sorting
        
        for d, v in zip(vehicleEmissionDates, vehicleEmissions):
            combinedEmissions[d] += float(v)
        
        for d, a in zip(applianceEmissionDates, applianceEmissions):
            combinedEmissions[d] += float(a)
            
        #now sort
        mergedResults = sorted(combinedEmissions.items())
        
        print(f"Combined Emissions by Date:\n{mergedResults}")
        
        """
        
        import inquirer
        from user_direct_class import direction_picklist
        graph_question = [
                    inquirer.List('Graph to View',
                                  message = f"Please select the emission graph you wish to view:",
                                  choices = ["Appliances", "Vehicles", "Both"],
                              ),
                    ]
        graph_answer = inquirer.prompt(graph_question)
        choice = graph_answer['Graph to View']
        if choice == "Appliances":
            user.graphAppliances(username, applianceEmissions, applianceEmissionDates)
            direction_picklist.page_direction(username)
        elif choice == "Vehicles":
            user.graphVehicles(username, vehicleEmissions, vehicleEmissionDates)
            direction_picklist.page_direction(username)
        elif choice == "Both":
            user.sortAllData(username)
        else:
            print("Error encountered, choice not recgonised./nPlease try again.")
            direction_picklist.page_direction(username)
            
        
    def sortAllData(username):
        """ Used To Retrieve and Combine Data From Both Appliances and Vehicles """
        import dbConnection
        import datetime
        from datetime import date
        #initialise variablaes
        global emissionValues
        global emissionDates
        emissionValues = []
        emissionDates = []
        #create SQL queries
        mycursor = dbConnection.db.cursor()
        applianceSQL = "SELECT total_emissions, date FROM appliance_logs WHERE user = %s"
        vehicleSQL = "SELECT value, date FROM car_emissions WHERE user = %s"
        username = ["Admin"] #for test purposes
        val = username
        #get appliance results
        mycursor.execute(applianceSQL, val)
        applianceResults = mycursor.fetchall()
        #get vehicle results
        mycursor.execute(vehicleSQL, val)
        vehicleResults = mycursor.fetchall()
        #merge into list
        data = []
        #print(vehicleResults)
        #print(applianceResults)
        data = applianceResults + vehicleResults
        #print(data)
        #print(f"The combined results are: {data}")
        
        """
        This section of code will merge any duplicate dates into one combined emission value
        """
        from collections import defaultdict
        
        non_duplicates = []
        duplicates = []
        
        grouped_date = defaultdict(list)
        for value, dates in data:
            grouped_date[dates].append((value, dates))
            
        for items in grouped_date.values():
            if len(items) > 1:
                duplicates.extend(items)
            else:
                non_duplicates.extend(items)
                
        #print(f"\nDuplicates: {duplicates}")
        #print(f"\nNon-duplicates: {non_duplicates}")
        
        
        cleaned_duplicates = []
        added_emissions = defaultdict(float)
        
        for value, dates in duplicates:
            added_emissions[dates] += value
            
        cleaned_duplicates = [(total, date) for date, total in added_emissions.items()]
        #print(f"\nCleaned duplicates = {cleaned_duplicates}")
            
        #now concatenate the non-duplicated and cleaned duplicated data together into one list
        data = cleaned_duplicates + non_duplicates
        #Sort the new list into chronological order before splitting and passing to graph function
        sorted_data = sorted(data, key=lambda x: x[1])
        #print(f"\nThe sorted data is: {sorted_data}")
        
        #split data into emissions and dates
        
        emissionValues = [item[0] for item in sorted_data] #iteration keeps emissions in date order
        emissionDates = [item[1] for item in sorted_data]
        emissionDates = [date.isoformat(item) for item in emissionDates] #strip datetime text from date
        
        #print(f"\nThe emission values are: {emissionValues}")
        #print(f"\nThe emission dates are: {emissionDates}")
        
        #call graphing function
        user.totalGraphing(username, emissionValues, emissionDates)
    
    def setLinkedUser(username):
        import dbConnection #to enable outreach to SQL database
        #take username of account to link to
        username2 = input("Please provide the username of the account you wish to link\n")
        cursor = dbConnection.db.cursor()
        sql = "SELECT pending_links FROM user_details WHERE username = %s"
        val = username,
        cursor.execute(sql, val) #execute the SQL query
        user_result = cursor.fetchall() #store sql result in variable
        print(user_result)
        for item in user_result:
            pending_list = [u.strip() for u in item[0].split(',') if u.strip()] #converts string to a list of usernames
            print(pending_list)
            if username2 in pending_list:
                print(f"Account linkage request awaiting review by {username}")
                from user_direct_class import direction_picklist
                direction_picklist.page_direction(username)
            else:
                import inquirer
                query_update = [
                    inquirer.List('Add linked user',
                                  message = f"Would you like to link your account to {username2}'s?",
                                  choices = ["Yes", "No"],
                              ),
                    ]
                query_answer = inquirer.prompt(query_update)
                choice = query_answer['Add linked user']
                if choice == "Yes":
                    
                    sql1 = "SELECT username FROM user_details WHERE username = %s"
                    val1 = username2,
                    cursor.execute(sql1, val1)
                    user_check = cursor.fetchone()
                    if username2 in user_check[0]:
                        """Update user 1"""
                        #IFNULL used below to concatenate, as otherwise you would often concatenate to a blank field which will not work
                        sql2 = "UPDATE user_details SET pending_links = CONCAT(IFNULL(pending_links, ''), ', ', %s) WHERE username = %s" #sending to pending links column to await approval
                        val2 = (username, username2)
                        cursor.execute(sql2, val2)
                        dbConnection.db.commit()
                        print(f"Account link request sent to {username} for approval")
                        from user_direct_class import direction_picklist
                        print("Please pick an action")
                        direction_picklist.page_direction(username)
                    else:
                        print("The user you are trying to link to has not been found, please try again")
                        user.setLinkedUser(username)

                
                else:
                    user.setLinkedUser(username)
     
    def approve_links(username):
        import dbConnection
        cursor = dbConnection.db.cursor()
        sql = "SELECT pending_links FROM user_details WHERE username = %s"
        val = (username,)
        cursor.execute(sql, val)
        pending_list = [] #initialises an empty list to store any pending approvals in after retrieval
        pending_results = cursor.fetchall()
        #strip any leading and trailing commas
        #pending_results = pending_results.lstrip(',')
        #pending_results = pending_results.rstrip(',')
        #print(pending_results)
        for item in pending_results:
            if item[0]:
                #item.append(pending_list)
                pending_list.extend([u.strip() for u in item[0].split(',') if u.strip()])
        print(pending_list)
        import inquirer
        query_link = [
                    inquirer.List('Approve Link',
                                  message = f"Would you like to link your account?",
                                  choices = ["Yes", "No"],
                              ),
                    ]
        query_answer = inquirer.prompt(query_link)
        """Now loop through pending_list and execute sql as needed """
        """
        for item in pending_list:
            print(f"You have a pending link request from {pending_list[0]}")
            choice = query_answer['Approve Link']
            if choice == "Yes":
                    sql = "UPDATE user_details SET linked_accounts = CONCAT(IFNULL(linked_accounts, ''), ', ', %s) WHERE username = %s"
                    val = (item, username)
                    cursor.execute(sql, val)
                    dbConnection.db.commit()
                    pending_list.remove(item)
            else:
                pending_list.remove(item)
        """
        
        #The below has a bug and will approve all requests regardless of how many are present, this will need rectifying
        while pending_list:
            item = pending_list.pop(0)    
            print(f"You have a pending link request from {item}")
            choice = query_answer['Approve Link']
            if choice == "Yes":
                    sql = "UPDATE user_details SET linked_accounts = CONCAT(IFNULL(linked_accounts, ''), ', ', %s) WHERE username = %s"
                    val = (item, username)
                    cursor.execute(sql, val)
                    dbConnection.db.commit()
        print("Your pending approvals: ")
        print(pending_list)
        print("Records updated.\nPlease pick an action:")
        from user_direct_class import direction_picklist
        direction_picklist.page_direction(username)
  
#user.forgot_password()
#user.sortAllData("Admin")

    def useVehicleAverage(username): #pull user vehicle averages and provide option to resubmit using a new date
        import dbConnection
        cursor = dbConnection.db.cursor()
        #create and execute sql statement
        sql = "SELECT drive_name FROM drive_averages WHERE user = %s"
        val = (username,)
        cursor.execute(sql, val)
        #manipulate sql returns into picklist
        drive_list = cursor.fetchall()
        #print(drive_list) #testing
        #store the route names and present them as picklist options
        route_names = [] #initiate list to store route names to be accessed by a picklist
        for item in drive_list:
            if item[0]:
                route_names.append(item[0])
        #print(route_names)#testing
        #now turn the route_names items into a picklist using tkinter
        import tkinter
        from tkinter import ttk
        root = tkinter.Tk()
        root.title("Please select your route") #sets up the window
        selected_route = tkinter.StringVar()
        #create the GUI
        combo = ttk.Combobox(root, values=route_names, state="readonly", textvariable=selected_route)
        combo.pack(padx=30, pady=30)
        combo.set("Please select your route")
        combo.bind("<<ComboboxSelected>>", lambda e: print(f"Selected inside GUI: {selected_route.get()}")) #used to allow us to reference the variable at a later date
        root.mainloop()
        my_route = selected_route.get()
        print(my_route) #to store the selected option from tkinter
        #now pull the relevant data from mysql
        sql2 = "SELECT vehicle_reg, drive_emission FROM drive_averages WHERE User = %s AND drive_name = %s"
        vals = (username, my_route)
        cursor.execute(sql2, vals)
        results = cursor.fetchone()
        #print(results)
        car_reg = results[0] #store car_reg value
        value = results[1] #store emissions value
        #print(car_reg)
        #print(value)
        """Retrieve date of drive using code taken from PetrolCarCalculator.carEmissionsCalculation"""
        import inquirer
        import datetime
        from datetime import date
        date_question = [
        inquirer.List('Date of Emission',
                      message = "Was ths emission from today?",
                      choices = [ "Yes","No"], #establish picklist
            ),
        ]
        date_answer = inquirer.prompt(date_question)
        choice = date_answer['Date of Emission']
     
        if choice == "Yes":
            date_of_emission = date.today() #use today's date
        else: #if drive not from today
            date_of_emission = input("Please input the date of these emissions: ")
            date_of_emission = datetime.datetime.strptime(date_of_emission, "%d/%m/%Y") #format the date based on user input
            
        """Now send data to SQL server"""
        sql3 = "INSERT INTO car_emissions (user, date, vehicle, value) VALUES (%s, %s, %s, %s)"
        val3 = (username, date_of_emission, car_reg, value)
        cursor.execute(sql3, val3)
        dbConnection.db.commit()
        print("Emission logged! Returning you to the main menu.")
        from user_direct_class import direction_picklist
        direction_picklist.page_direction(username) #send user back to the main menu