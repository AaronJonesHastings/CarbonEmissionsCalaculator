import dbConnection
import datetime
import bcrypt

def hash_password(password):
    """
    from the hashingAndSalting.py file
    """
    #Generate the salt
    salt = bcrypt.gensalt()
    #now hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt) #define encryption (UTF-8) and combine with salt
    print(hashed_password)
    return hashed_password

def userSignUp():
    """
    Take user inputs to be stored in SQL table. Password will be passed to the salt and hash
    functions from hashingAndSalting.py
    """
    Forename = input("Please enter your first name: ")
    Surname = input("Please enter your surname: ")
    email = input("Please provide an email address :")
    dob = input("Please enter your date of birth (dd/mmm/YYYY): ")
    useableDOB = datetime.datetime.strptime(dob, "%d/%m/%Y") #Format DOB
    username = input("Please enter a username: ")
    #Check if user already exists
    cursor = dbConnection.db.cursor() #get cursor from dbConnection.py
    sql = "SELECT username FROM user_details WHERE username = %s" #SQL query to pass
    cursor.execute(sql, (username,)) #execute the SQL
    result = cursor.fetchone() #store restult in variable
    if result: #user exists, redirect to login screen
        
        print("User already exists, please try logging in")
        from login import verify_password
        
    else: #if user does not exist
        import getpass #used to hide password input
        import string
        while True:
            password = getpass.getpass("Please enter your chosen password:\n")
            is_valid = all(( #check all 4 conditions below are met
                len(password) >= 8,#check character length is at least 8 
                any(c.isalpha() for c in password), #checks for the presence of an alpha character
                any(c.isdigit() for c in password), #checks for a numeric character
                any(c in string.punctuation for c in password) #checks for a special character
            ))
            if is_valid:
                break
            print("Password must contain a number and special character, and be at least 8 characters long\n")
        verify_password = getpass.getpass("Please enter your password again:\n")
        if verify_password == password: #check that first passowrd input matches the second password input
            salt = bcrypt.gensalt() #generate the salt
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt) #encrpy the password using utf-8 and attach the salt
            #print(hashed_password) #testing
            mycursor = dbConnection.db.cursor()
            sql = "INSERT INTO user_details (forename, surname, dob, username, password, email) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (Forename, Surname, useableDOB, username, hashed_password, email)
            mycursor.execute(sql, val) #execute the SQL statement
            dbConnection.db.commit() #commit changes
            print(mycursor.rowcount, "record inserted") #confirmation
            #take security question and answer after account creation
            sq = input("Please set a security question. This will be used if you forget your password:\n")
            sa = input("Please provide the answer to your security question (please note that this answer is case sensitive):\n")
            sql2 = "UPDATE user_details SET security_question = %s, security_answer = %s WHERE username = %s"
            val2 = (sq, sa, username)
            mycursor = dbConnection.db.cursor() #send security Q+A to SQL server
            mycursor.execute(sql2, val2)
            dbConnection.db.commit()
            print(mycursor.rowcount, "record inserted")
            print("Thank you for signing up to use your personal carbon emissions calculator!\nYou may now sign in") #confirmation of process end
            login_attempts = 0
            from login import verify_password
            verify_password(username, login_attempts) #log user in
        else:
            print ("Passwords do not match")
            userSignUp() #loop back to start
    
#userSignUp()
