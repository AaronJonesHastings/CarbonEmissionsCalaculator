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
                    newPassword = input("Please enter your new password: ")
                    if len(newPassword) < 10:
                        print("Password must be 10 charcaters or greater")
                        return user.change_password()
                    else:
                        comparePassword = input("Please enter your new password again: ")
                        if newPassword != comparePassword:
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
                print("Error encountered, please try again or contact support")
                return
        
        else:
            print("Error: user not found, please try again or contact support")
            return
    
    def forgot_password():
        #used when a user does not know their password
        import dbConnection
        mycursor = dbConnection.db.cursor()
        username = input("Please enter your username:\n")
        email = input("Please enter your email address:\n")
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
                newPassword = input("Please enter your new password: ")
                if len(newPassword) < 10:
                    print("Password must be 10 charcaters or greater")
                    return user.forgot_password()
                else:
                    comparePassword = input("Please enter your new password again: ")
                    if newPassword != comparePassword:
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
            else:
                print("Your answer does not match our reords. Please contact support for further assistance, or try again.")
        else:
            print("No user found, please try again")
            
    def lockout(username):
        import dbConnection
        sql = "UPDATE user_details SET locked = %s WHERE username = %s"
        locked = '1'
        val = (locked, username)
        mycursor = dbConnection.db.cursor()
        mycursor.execute(sql, val)
        dbConnection.db.commit()
        print("Account locked due to too many inorrect password entries. Please contact support to unlock your account, or select forgot password")
        
    def graphAppliances(username, applianceEmissions, applianceEmissionDates):
        import matplotlib.pyplot as plt
        #separate out dates and floats in the emission lists returned from retrieveEmissions function
        plt.plot (applianceEmissionDates, applianceEmissions)
        #set title and labels
        plt.title("Appliance Emissions Trending") #graph title
        plt.xlabel("Date") #x axis label
        plt.ylabel("Co2 Emissions") #y axis label
        
        plt.grid(True)
        plt.show() #show the graph
        
    def graphVehicles(username, vehicleEmissions, vehicleEmissionDates):
        import matplotlib.pyplot as plt
        #separate out dates and floats in the emission lists returned from retrieveEmissions function
        plt.plot (vehicleEmissionDates, vehicleEmissions)
        plt.title("Vehicle Emissions Trending")
        plt.xlabel("Date")
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
        plt.ylabel("Co2 Emissions Per Day (kg)")
        style.use("ggplot")
        plt.grid(True)
        plt.show()
    
    def retrieveEmissionsWithDate(username):
        import dbConnection
        from datetime import date
        mycursor = dbConnection.db.cursor()
        """retrieve all emissions from the appliance_logs and car_emissions table"""
        #create lists for storing emission returns
        global applianceEmissions
        applianceEmissions = []
        global vehicleEmissions
        vehicleEmissions = []
        
        #SQL query for appliance emission values
        applianceSQL = "SELECT total_emissions, date FROM appliance_logs WHERE user = %s"
        val = (username,) #val to be used for car and appliance queries
        mycursor.execute(applianceSQL, val,)
        applianceResult = mycursor.fetchall() #store SQL returns
        #print("Total number of appliance emission records = ", mycursor.rowcount)

        #iterate through the result and add to the emissionResults list
        n = 0
        for i in applianceResult:
            applianceEmissions.append(applianceResult[n])
            n = n+1 
        #print(applianceEmissions)

        #SQL query for car emissions
        vehicleSQL = "SELECT value, date FROM car_emissions WHERE user = %s"
        mycursor.execute(vehicleSQL, val,)
        vehicleResult = mycursor.fetchall()
        #print("Total number of vehcile emissions = ", mycursor.rowcount)

        #iterate through vehcicle emission returns and store in vehicleEmissions
        n = 0
        for i in vehicleResult:
            vehicleEmissions.append(vehicleResult[n])
            n = n+1
        #print(vehicleEmissions)
             
        data = vehicleEmissions #store data in separate lists
        #print("Separated Data")
        
        sorted_data = sorted(data, key=lambda x: x[1])
        
        vehicleEmissionDates = [item[1] for item in sorted_data] #separate dates from emissions
        vehicleEmissionDates = [date.isoformat(item) for item in vehicleEmissionDates] #format dates appropriately
        
        
        vehicleEmissions = [item[0] for item in sorted_data]
        
        print(f"Vehicle Emissions = {vehicleEmissions}")
        print(f"Vehicle Emission Dates = {vehicleEmissionDates}")
        
        #repeat above for appliance emissions
        data2 = applianceEmissions
        sorted_data2 = sorted(data, key=lambda x: x[1])
        applianceEmissionDates = [item[1] for item in sorted_data2]
        applianceEmissionDates = [date.isoformat(item) for item in applianceEmissionDates]
        applianceEmissions = [item[0] for item in sorted_data2]
        
        print(f"Appliance emissions = {applianceEmissions}")
        print(f"Appliance emission dates = {applianceEmissionDates}")
        
        user.graphAppliances(username, applianceEmissions, applianceEmissionDates)
        user.graphVehicles(username, vehicleEmissions, vehicleEmissionDates)
        
    def sortAllData(username):
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
                
        print(f"\nDuplicates: {duplicates}")
        print(f"\nNon-duplicates: {non_duplicates}")
        
        
        cleaned_duplicates = []
        added_emissions = defaultdict(float)
        
        for value, dates in duplicates:
            added_emissions[dates] += value
            
        cleaned_duplicates = [(total, date) for date, total in added_emissions.items()]
        print(f"\nCleaned duplicates = {cleaned_duplicates}")
            
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
        
  
#user.forgot_password()
user.sortAllData("Admin")   