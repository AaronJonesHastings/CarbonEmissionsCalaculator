import dbConnection #imports the database details
import bcrypt #library used for decryption
global login_attempts

#get user details at login

#username = input("Please enter your username: ")

#login_attempts = 0 #locks account when login_attempts = 3

#define the variable to verify the password
def verify_password(username, login_attempts):
    #login_attempts = 0
    import getpass
    password = getpass.getpass("Please enter your password:\n") #getpass used to blank out password during entry
    cursor = dbConnection.db.cursor()
    exists_check = "SELECT username FROM user_details WHERE username = %s" #confirm user exists
    val = (username,)
    cursor.execute(exists_check, val)
    result = cursor.fetchone() #result in SQL table
    if result:
        lockout = 0 #set lockout value to 0 and initiate the lockout variable
        locked_query = "SELECT locked FROM user_details WHERE username = %s" #confirm account is not locked
        val = (username,)
        cursor.execute(locked_query, val)
        locked = cursor.fetchone() #store result of locked query
        #print(locked) #test print
        if locked == (0,):
            if login_attempts < 3:
                #username = input("Please enter your username")
                #password = input("Please enter your password")
                sql = "SELECT password FROM user_details WHERE username = %s" #SQL query to pass
                cursor = dbConnection.db.cursor() #get cursor from dbConnection.py
                cursor.execute(sql, (username,)) #execute the SQL. Passing named parameters for safety (SQL injections)
                result = cursor.fetchone() #store restult in variable

                if result:
                    stored_hash = result[0].encode('utf-8') #get hash in bytes
                    #now verify the password against the stored hash
                    if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                        print("Password Accepted\n")
                        """Small bit of code to greet the user with their name"""
                        name_sql = "SELECT forename FROM user_details WHERE username = %s" #pull forename from SQL table
                        name_val = (username,) #qualifier for SQL
                        cursor.execute(name_sql, name_val) #execute SQL
                        forename = cursor.fetchone() #pull forename
                        #clean forname before printing
                        forename = str(forename).strip('(),')
                        forename = forename.replace("'", "")
                        print(f"Welcome back {forename}!") #print greeting
                        #direct user to main menu using direction_picklist class
                        from user_direct_class import direction_picklist
                        direction_picklist.page_direction(username)
                        #return True #decrypt successful
                    else:
                        print("Password Not Accepted\n")
                        login_attempts = login_attempts + 1
                        print(f"New login attempts value = {login_attempts}")
                        return verify_password(username, login_attempts) #decrpyt failed
                else:
                    print("User Not Found\n")
                    return False #no match in user_details table
            else:
                #following lines direct user to fixing their lockout based on the choices they select
                print("Your account is locked, please contact support or use the forgotten password function")
                import inquirer
                lockout_question = [
                    inquirer.List ('Unlock Choices',
                           message = 'Please select unlock acount, forgotten password or close application:',
                           choices = ["Forgotten password", "Unlock account", "Close application"],
                    ),
                ]
            
                account_management_answer = inquirer.prompt(lockout_question)
                account_choice = (account_management_answer['Unlock Choices'])
                if account_choice == "Forgotten password":
                    from userClass import user
                    user.forgot_password()
                elif account_choice == "Unlock account":
                    from userClass import user
                    user.unlockAccount(username)
                elif account_choice == "Close application":
                    exit()
                else:
                    print("Error encountered, please attempt to login again, or contact support\n")
                    take_username()

        else:
            print("Your account is locked, please contact support or use the forgotten password function\n")
            import inquirer
            lockout_question = [
                inquirer.List ('Unlock Choices',
                               message = 'Please select unlock acount, forgotten password or close application:',
                               choices = ["Forgotten password", "Unlock account", "Close application"],
                           ),
                ]
            
            account_management_answer = inquirer.prompt(lockout_question)
            account_choice = (account_management_answer['Unlock Choices'])
            if account_choice == "Forgotten password":
                from userClass import user
                user.forgot_password()
            elif account_choice == "Unlock account":
                from userClass import user
                user.unlockAccount(username)
            elif account_choice == "Close application":
                exit()
                
    else:
        import inquirer
        #determine if user's average should be used for the day's emission calculation
        create_question = [
            inquirer.List ('create_account',
                           message = "User does not exist, would you like to create an account?\n",
                           choices = [ "Yes", "No"],
            ),
        ]

        create_answer = inquirer.prompt(create_question)
    
        choice = (create_answer['create_account'])
        if choice == "Yes":
            from userSignUp import userSignUp
            userSignUp()
        else:
            return
            
def take_username():
    username = input("Please enter your username:\n")
    login_attempts = 0 #locks account when login_attempts = 3
    return verify_password(username, login_attempts)