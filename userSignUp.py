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
        
    else: #result not found in SQL table
        password = input("Please enter a your chosen password:\n")
        verify_password = input("Please enter your password again:\n")
        if verify_password == password:
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            print(hashed_password)
            mycursor = dbConnection.db.cursor()
            sql = "INSERT INTO user_details (forename, surname, dob, username, password, email) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (Forename, Surname, useableDOB, username, hashed_password, email)
            mycursor.execute(sql, val)
            dbConnection.db.commit()
            print(mycursor.rowcount, "record inserted")
            sq = input("Please set a security question. This will be used if you forget your password:\n")
            sa = input("Please provide the answer to your security question (please note that this answer is case sensitive):\n")
            sql2 = "UPDATE user_details SET security_question = %s, security_answer = %s WHERE username = %s"
            val2 = (sq, sa, username)
            mycursor = dbConnection.db.cursor()
            mycursor.execute(sql2, val2)
            dbConnection.db.commit()
            print(mycursor.rowcount, "record inserted")
            print("Thank you for signing up to use your personal carbon emissions calculator!\nYou may now sign in")
            login_attempts = 0
            from login import verify_password
            verify_password(username, login_attempts)
        else:
            print ("Passwords do not match")
            userSignUp() #loop back to start
    
#userSignUp()
